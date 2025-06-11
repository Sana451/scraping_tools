import os
import requests
import logging
import time

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

TELEGRAM_DOMAIN = os.getenv("TELEGRAM_DOMAIN", "https://api.telegram.org")
BOT_TOKEN = "7680351688:AAGC7eRCpQNkRkoCVy-4yjQeuG1BDwkSjoE"
CHAT_ID = "1748157760"

# Общий таймаут для всех запросов
REQUEST_TIMEOUT = 5  # секунд


def send_file_result(file_name, bot_token=BOT_TOKEN, chat_id=CHAT_ID, caption="Результат парсинга"):
    """Отправляет файл в Telegram с логированием и защитой от зависаний."""
    start_time = time.time()
    logger.info(f"Начинаю отправку файла: {file_name} -> Telegram чат {chat_id}")

    if not os.path.exists(file_name):
        logger.error(f"Файл не найден: {file_name}")
        return

    try:
        with open(file_name, 'rb') as file:
            response = requests.post(
                url=f"{TELEGRAM_DOMAIN}/bot{bot_token}/sendDocument",
                data={
                    "chat_id": chat_id,
                    "caption": caption,
                },
                files={"document": file},
                timeout=REQUEST_TIMEOUT
            )

        duration = time.time() - start_time
        if response.status_code == 200:
            logger.info(f"Файл {file_name} успешно отправлен за {duration:.2f} сек.")
            print(f"✅ Файл {file_name} успешно отправлен.")
        else:
            logger.error(f"❌ Ошибка при отправке файла {file_name}: HTTP {response.status_code}, ответ: {response.text}")

        return response.json()

    except requests.exceptions.Timeout:
        logger.error(f"⏱ Превышено время ожидания при отправке файла {file_name} (таймаут {REQUEST_TIMEOUT}s)")
    except requests.exceptions.RequestException as error:
        logger.error(f"❌ Ошибка сети при отправке файла {file_name}: {error}")
    except Exception as e:
        logger.exception(f"❗️Непредвиденная ошибка при отправке файла {file_name}: {e}")


def send_telegram_log(message="Not message to send but I wanted it too much.", bot_token=BOT_TOKEN, chat_id=CHAT_ID):
    """Отправляет текстовое сообщение в Telegram с таймаутом и логами."""
    start_time = time.time()
    logger.info(f"Отправка Telegram-сообщения: {message[:50]}...")

    try:
        response = requests.post(
            url=f"{TELEGRAM_DOMAIN}/bot{bot_token}/sendMessage",
            data={
                "chat_id": chat_id,
                "text": message
            },
            timeout=REQUEST_TIMEOUT
        )

        duration = time.time() - start_time
        if response.status_code == 200:
            logger.info(f"Сообщение успешно отправлено за {duration:.2f} сек.")
            print(f"📨 Сообщение отправлено: {message[:50]}...")
        else:
            logger.error(f"❌ Ошибка отправки сообщения: HTTP {response.status_code}, ответ: {response.text}")

        return response.json()

    except requests.exceptions.Timeout:
        logger.error(f"⏱ Превышено время ожидания при отправке сообщения (таймаут {REQUEST_TIMEOUT}s)")
    except requests.exceptions.RequestException as error:
        logger.error(f"❌ Ошибка сети при отправке сообщения: {error}")
    except Exception as e:
        logger.exception(f"❗️Непредвиденная ошибка при отправке сообщения: {e}")


if __name__ == '__main__':
    send_file_result(file_name=__file__)
    send_telegram_log("Тестовое сообщение из main")
