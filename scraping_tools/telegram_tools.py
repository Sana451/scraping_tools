import io
import logging
import os
import requests
import time

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

TELEGRAM_DOMAIN = os.getenv("TELEGRAM_DOMAIN", "https://api.telegram.org")
BOT_TOKEN = "7680351688:AAGC7eRCpQNkRkoCVy-4yjQeuG1BDwkSjoE"
CHAT_ID = (1748157760, 7606152113)

# Общий таймаут для всех запросов
REQUEST_TIMEOUT = 5  # секунд


def send_file_result(
        file_name,
        bot_token=BOT_TOKEN,
        chat_id=CHAT_ID,
        caption="Результат парсинга"
):
    """Отправляет файл в Telegram одному или нескольким получателям."""
    start_time = time.time()
    logger.info(f"Начало отправки файла: {file_name} -> Telegram чат(ы): {chat_id}")

    if not os.path.exists(file_name):
        logger.error(f"Файл не найден: {file_name}")
        return

    # Преобразуем chat_id в список, если передан один ID
    chat_ids = chat_id if isinstance(chat_id, (list, tuple)) else [chat_id]

    try:
        with open(file_name, "rb") as file:
            file_bytes = file.read()  # читаем один раз, чтобы не открывать файл заново

        for cid in chat_ids:
            with io.BytesIO(file_bytes) as f:
                f.name = os.path.basename(file_name)  # Telegram требует имя файла
                response = requests.post(
                    url=f"{TELEGRAM_DOMAIN}/bot{bot_token}/sendDocument",
                    data={"chat_id": cid, "caption": caption},
                    files={"document": f},
                    timeout=REQUEST_TIMEOUT,
                )

            if response.status_code == 200:
                logger.info(f"Файл {file_name} успешно отправлен в чат {cid}")
            else:
                logger.error(f"Ошибка при отправке файла {file_name} в чат {cid}: "
                             f"HTTP {response.status_code}, ответ: {response.text}")

        duration = time.time() - start_time
        logger.info(f"Отправка файла завершена за {duration:.2f} сек.")

    except Exception as e:
        logger.error(f"Ошибка при отправке файла {file_name}: {type(e).__name__} — {e}")


def send_telegram_log(
        message="Not message to send but I wanted it too much.",
        bot_token=BOT_TOKEN,
        chat_id=CHAT_ID,
):
    """
    Отправляет текстовое сообщение в Telegram.
    Поддерживает один chat_id (int/str) или несколько (list/tuple).
    """
    start_time = time.time()
    logger.info(f"Отправка Telegram-сообщения: {message[:50]}...")

    # Приводим chat_id к списку для единообразной обработки
    chat_ids = [chat_id] if isinstance(chat_id, (int, str)) else list(chat_id)

    results = []

    for cid in chat_ids:
        try:
            response = requests.post(
                url=f"{TELEGRAM_DOMAIN}/bot{bot_token}/sendMessage",
                data={"chat_id": cid, "text": message},
                timeout=REQUEST_TIMEOUT
            )

            duration = time.time() - start_time
            if response.status_code == 200:
                logger.info(f"Сообщение успешно отправлено в чат {cid} за {duration:.2f} сек.")
            else:
                logger.error(
                    f"Ошибка отправки сообщения в чат {cid}: HTTP {response.status_code}, ответ: {response.text}")

            results.append(response.json())

        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения в чат {cid}: {type(e).__name__} — {e}")
            results.append({"chat_id": cid, "error": str(e)})

    return results


if __name__ == '__main__':
    send_file_result(file_name=__file__)
    send_telegram_log("Тестовое сообщение из telegram.tools.main")
