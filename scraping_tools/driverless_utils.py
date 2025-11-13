import json
import os
import re
import time
from pathlib import Path

from selenium_driverless.sync import webdriver
from selenium_driverless.types.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium_driverless.types.webelement import NoSuchElementException
from twocaptcha import TwoCaptcha

api_key = os.getenv('APIKEY_2CAPTCHA', '2678f4ff49e147589ed9870098b6d271')

solver = TwoCaptcha(api_key)


def create_driver(proxy: str | None = None, headless: bool = False):
    """
    Создаёт экземпляр selenium-driverless Chrome с опциональным прокси и headless-режимом.

    :param proxy: строка прокси в формате 'http://user:pass@host:port' или None
    :param headless: запуск без окна браузера
    :return: webdriver.Chrome
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-features=DisableLoadExtensionCommandLineSwitch")
    options.add_argument("--start-maximized")

    # Явно добавляем headless-режим при необходимости
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)

    if proxy:
        driver.set_single_proxy(proxy)

    return driver



async def load_cookies(driver, filename: str, url: str):
    """Загружает cookies из JSON-файла"""
    if not Path(filename).exists():
        print(f"Файл {filename} не найден, пропускаем загрузку")
        return

    with open(filename, "r", encoding="utf-8") as f:
        cookies = json.load(f)

    # Нужно сначала открыть сайт, чтобы домен совпадал
    await driver.get(url)
    for cookie in cookies:
        try:
            # удаляем поля, которые Selenium не принимает напрямую
            cookie.pop("sameParty", None)
            cookie.pop("sourceScheme", None)
            cookie.pop("sourcePort", None)
            await driver.add_cookie(cookie)
        except Exception as e:
            print(f"Ошибка добавления cookie {cookie.get('name')}: {e}")
    print(f"Загружено {len(cookies)} cookies из {filename}")
    return cookies


async def save_cookies(driver, filename: str):
    """Сохраняет cookies в JSON-файл"""
    cookies = await driver.get_cookies()
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(cookies, f, ensure_ascii=False, indent=2)
    print(f"Cookies сохранены в {filename}")


def normalize_proxy_uri_for_datadome_captcha_solver(proxy: str) -> str:
    """
    Проверяет и нормализует строку прокси.
    Удаляет префикс http:// или https://, если он есть.

    :param proxy: строка вида "http://user:pass@1.2.3.4:8080" или "user:pass@1.2.3.4:8080"
    :return: строка вида "user:pass@1.2.3.4:8080"
    :raises ValueError: если формат прокси некорректный
    """
    if not isinstance(proxy, str) or not proxy.strip():
        raise ValueError("Proxy must be a non-empty string")

    # убираем протокол
    proxy = proxy.strip()
    proxy = proxy.replace("http://", "").replace("https://", "")

    # базовая проверка формата user:pass@ip:port
    pattern = r"^[^:@]+:[^:@]+@[\w\.-]+:\d+$"
    if not re.match(pattern, proxy):
        raise ValueError(f"❌ Invalid proxy format: {proxy}")

    return proxy


def solve_datadome_captcha_if_present(driver: webdriver, proxy_uri: str):
    proxy_uri = normalize_proxy_uri_for_datadome_captcha_solver(proxy_uri)

    try:
        print("Waiting for CAPTCHA")
        wait_for_element(driver, By.XPATH, "//*[@title='DataDome CAPTCHA']", timeout=10)
        print("Found CAPTCHA on page")

        try:
            print("Start solving CAPTCHA")
            iframe = driver.find_element(By.XPATH, "//*[@title='DataDome CAPTCHA']")
            captcha_url = iframe.get_attribute("src")
            print(captcha_url)
            pageurl = driver.current_url
            print(pageurl)
            userAgent = driver.execute_script("return navigator.userAgent;")
            print(userAgent)
            result = solver.datadome(
                captcha_url=captcha_url,
                pageurl=pageurl,
                userAgent=userAgent,
                proxy={
                    'type': 'HTTP',
                    'uri': proxy_uri  # 'login:password@IP_address:PORT'
                }
            )
            print("Solved CAPTCHA")
            cookie_value = result["code"].split("datadome=")[1].split(";")[0]
            driver.add_cookie(
                {
                    "name": "datadome",
                    "value": cookie_value,
                    "domain": ".rubix.com",
                    "path": "/",
                    "secure": True,
                }
            )
            print("Added CAPTCHA solution to cookies")
            driver.refresh()
            print("Refreshed page with solved CAPTCHA")

        except Exception as e:
            print(f"Error while solving CAPTCHA {e}")

    except Exception:
        print("Not found CAPTCHA on page")


async def solve_datadome_captcha_if_present_async(driver: webdriver, proxy_uri: str, timeout=10):
    proxy_uri = normalize_proxy_uri_for_datadome_captcha_solver(proxy_uri)

    try:
        print("Waiting for CAPTCHA")
        await wait_for_element_async(
            driver, By.XPATH,
            "//*[@title='DataDome CAPTCHA']",
            timeout=timeout
        )
        print("Found CAPTCHA on page")

        try:
            print("Start solving CAPTCHA")
            iframe = await driver.find_element(By.XPATH, "//*[@title='DataDome CAPTCHA']")
            captcha_url = await iframe.get_attribute("src")
            print(captcha_url)
            pageurl = await driver.current_url
            print(pageurl)
            userAgent = await driver.execute_script("return navigator.userAgent;")
            print(userAgent)
            result = solver.datadome(
                captcha_url=captcha_url,
                pageurl=pageurl,
                userAgent=userAgent,
                proxy={
                    'type': 'HTTP',
                    'uri': proxy_uri  # 'login:password@IP_address:PORT'
                }
            )
            print("Solved CAPTCHA")
            cookie_value = result["code"].split("datadome=")[1].split(";")[0]
            await driver.add_cookie(
                {
                    "name": "datadome",
                    "value": cookie_value,
                    "domain": ".rubix.com",
                    "path": "/",
                    "secure": True,
                }
            )
            print("Added CAPTCHA solution to cookies")
            await driver.refresh()
            print("Refreshed page with solved CAPTCHA")

        except Exception as e:
            print(f"Error while solving CAPTCHA {e}")

    except Exception:
        print("Not found CAPTCHA on page")


def wait_for_element(driver: webdriver, by: By, value: str, timeout: int = 10, interval: float = 0.5):
    """
    Ожидание появления элемента на странице (аналог WebDriverWait).

    :param driver: экземпляр selenium_driverless.webdriver.Chrome
    :param by: способ поиска (например, By.ID, By.XPATH)
    :param value: значение для поиска
    :param timeout: сколько секунд ждать максимум
    :param interval: интервал между попытками
    :raises TimeoutError: если элемент не найден за отведённое время
    """
    start_time = time.time()

    while True:
        try:
            element = driver.find_element(by, value, timeout=1)
            if element:
                return element
        except NoSuchElementException:
            pass
        except Exception as e:
            print(f"[wait_for_element] retry due to: {e}")

        if time.time() - start_time > timeout:
            raise TimeoutError(f"Элемент не найден за {timeout} секунд: {by}={value}")

        driver.sleep(interval)


async def wait_for_element_async(
        driver: webdriver.Chrome,
        by: By,
        value: str,
        timeout: int = 10,
        interval: float = 0.5
) -> WebElement:
    """
    Ожидание появления элемента на странице (аналог WebDriverWait).

    :param driver: экземпляр selenium_driverless.webdriver.Chrome
    :param by: способ поиска (например, By.ID, By.XPATH)
    :param value: значение для поиска
    :param timeout: сколько секунд ждать максимум
    :param interval: интервал между попытками
    :return: найденный элемент (WebElement)
    :raises TimeoutError: если элемент не найден за отведённое время
    """
    start_time = time.time()

    while True:
        try:
            element = await driver.find_element(by, value, timeout=1)
            if element:
                return element
        except NoSuchElementException:
            pass
        except Exception as e:
            print(f"[wait_for_element_async] retry due to: {e}")

        if time.time() - start_time > timeout:
            raise TimeoutError(f"Элемент не найден за {timeout} секунд: {by}={value}")

        await driver.sleep(interval)
