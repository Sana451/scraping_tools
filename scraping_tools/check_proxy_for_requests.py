import requests
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List

test_url = "https://httpbin.org/ip"

OK = []
MISMATCH = []
DEAD = []

def parse_proxy(line: str) -> dict:
    line = line.strip()
    proxy_ip = ""

    # Формат 1: ip:port:user:pass
    if re.match(r"^\d+\.\d+\.\d+\.\d+:\d+:\S+:\S+$", line):
        ip, port, user, pwd = line.split(":")
        proxy_ip = ip
        proxy_url = f"http://{user}:{pwd}@{ip}:{port}"

    # Формат 2: user:pass@ip:port
    elif re.match(r"^\S+:\S+@\d+\.\d+\.\d+\.\d+:\d+$", line):
        creds, address = line.split("@")
        user, pwd = creds.split(":")
        ip, port = address.split(":")
        proxy_ip = ip
        proxy_url = f"http://{user}:{pwd}@{ip}:{port}"

    # Формат 3: ip:port (без авторизации)
    elif re.match(r"^\d+\.\d+\.\d+\.\d+:\d+$", line):
        ip, port = line.split(":")
        proxy_ip = ip
        proxy_url = f"http://{ip}:{port}"

    else:
        raise ValueError(f"❌ Неизвестный формат прокси: {line}")

    return {
        "proxy_ip": proxy_ip,
        "proxy_url": proxy_url
    }

def check_proxy(proxy_raw: str):
    try:
        parsed = parse_proxy(proxy_raw)
        proxy_ip = parsed["proxy_ip"]
        proxy_url = parsed["proxy_url"]

        proxies = {
            "http": proxy_url,
            "https": proxy_url,
        }

        response = requests.get(test_url, proxies=proxies, timeout=15)
        response_ip = response.json().get("origin", "")

        if proxy_ip in response_ip:
            OK.append(proxy_raw)
            print(f"✅ Proxy OK: {proxy_ip} == {response_ip}")
        else:
            MISMATCH.append(proxy_raw)
            print(f"⚠️  Proxy mismatch: {proxy_ip} != {response_ip}")

    except Exception as e:
        DEAD.append(proxy_raw)
        print(f"❌ Proxy is dead or invalid: {proxy_raw} | Error: {e}")

def main():
    with open("/home/sana451/PycharmProjects/scrapy_parsers/proxy.txt", "r", encoding="utf-8") as f:
        proxy_list = [line.strip() for line in f if line.strip()]

    print(f"🔍 Проверка {len(proxy_list)} прокси...")

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(check_proxy, proxy) for proxy in proxy_list]
        for _ in as_completed(futures):
            pass

    print("\n📊 Результаты:")
    print(f"Всего: {len(proxy_list)}")
    print(f"✅ Рабочих: {len(OK)}")
    print(f"⚠️  Несовпадение IP: {len(MISMATCH)}")
    print(f"❌ Нерабочих: {len(DEAD)}")

    # Если нужно, можно сохранить в файлы:
    with open("ok.txt", "w") as f:
        f.writelines(p + "\n" for p in OK)

    with open("mismatch.txt", "w") as f:
        f.writelines(p + "\n" for p in MISMATCH)

    with open("dead.txt", "w") as f:
        f.writelines(p + "\n" for p in DEAD)

if __name__ == "__main__":
    main()
