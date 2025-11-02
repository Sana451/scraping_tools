import io
import logging
import os
import requests
import time
from typing import Union, List, Tuple, Optional

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

REQUEST_TIMEOUT = 5  # Общий таймаут для всех запросов (секунд)


class TelegramClient:
    """
    Клиент для работы с Telegram Bot API.
    """

    def __init__(
            self,
            bot_token: str,
            chat_ids: Optional[Union[int, str, List, Tuple]] = None,
            telegram_domain: str = "https://api.telegram.org",
            request_timeout: int = 5
    ):
        """
        Инициализация клиента Telegram.

        :param bot_token: Токен бота Telegram
        :param chat_ids: ID чата/чатов для отправки (может быть int, str, list или tuple)
        :param telegram_domain: Домен Telegram API (по умолчанию https://api.telegram.org)
        :param request_timeout: Таймаут запросов в секундах
        """
        self.bot_token = bot_token
        self.chat_ids = chat_ids
        self.telegram_domain = telegram_domain
        self.request_timeout = request_timeout

        logger.info(f"TelegramClient инициализирован для бота с токеном: {bot_token[:10]}...")

    def send_file(
            self,
            file_name: str,
            chat_ids: Optional[Union[int, str, List, Tuple]] = None,
            caption: str = "Результат парсинга"
    ) -> List[dict]:
        """
        Отправляет файл в Telegram одному или нескольким получателям.

        :param file_name: Путь к файлу для отправки
        :param chat_ids: ID чата/чатов (если None, использует chat_ids из инициализации)
        :param caption: Подпись к файлу
        :return: Список результатов отправки для каждого чата
        """
        start_time = time.time()
        logger.info(f"Начало отправки файла: {file_name}")

        # Используем переданные chat_ids или те, что были при инициализации
        target_chat_ids = chat_ids if chat_ids is not None else self.chat_ids

        if target_chat_ids is None:
            logger.error("Не указаны chat_ids для отправки файла")
            return []

        if not os.path.exists(file_name):
            logger.error(f"Файл не найден: {file_name}")
            return []

        # Преобразуем chat_ids в список
        chat_ids_list = self._normalize_chat_ids(target_chat_ids)
        results = []

        try:
            with open(file_name, "rb") as file:
                file_bytes = file.read()

            for chat_id in chat_ids_list:
                result = self._send_single_file(chat_id, file_bytes, file_name, caption)
                results.append(result)

            duration = time.time() - start_time
            logger.info(f"Отправка файла завершена за {duration:.2f} сек.")

        except Exception as e:
            logger.error(f"Ошибка при отправке файла {file_name}: {type(e).__name__} — {e}")
            results.append({"error": str(e)})

        return results

    def send_message(
            self,
            message: str = "Not message to send but I wanted it too much.",
            chat_ids: Optional[Union[int, str, List, Tuple]] = None
    ) -> List[dict]:
        """
        Отправляет текстовое сообщение в Telegram.

        :param message: Текст сообщения
        :param chat_ids: ID чата/чатов (если None, использует chat_ids из инициализации)
        :return: Список результатов отправки для каждого чата
        """
        start_time = time.time()
        logger.info(f"Отправка Telegram-сообщения: {message[:50]}...")

        # Используем переданные chat_ids или те, что были при инициализации
        target_chat_ids = chat_ids if chat_ids is not None else self.chat_ids

        if target_chat_ids is None:
            logger.error("Не указаны chat_ids для отправки сообщения")
            return []

        # Преобразуем chat_ids в список
        chat_ids_list = self._normalize_chat_ids(target_chat_ids)
        results = []

        for chat_id in chat_ids_list:
            result = self._send_single_message(chat_id, message, start_time)
            results.append(result)

        return results

    def _send_single_file(
            self,
            chat_id: Union[int, str],
            file_bytes: bytes,
            file_name: str,
            caption: str
    ) -> dict:
        """Отправляет файл в один чат."""
        try:
            with io.BytesIO(file_bytes) as f:
                f.name = os.path.basename(file_name)
                response = requests.post(
                    url=f"{self.telegram_domain}/bot{self.bot_token}/sendDocument",
                    data={"chat_id": chat_id, "caption": caption},
                    files={"document": f},
                    timeout=self.request_timeout,
                )

            if response.status_code == 200:
                logger.info(f"Файл {file_name} успешно отправлен в чат {chat_id}")
                return {"chat_id": chat_id, "status": "success", "response": response.json()}
            else:
                logger.error(f"Ошибка при отправке файла {file_name} в чат {chat_id}: "
                             f"HTTP {response.status_code}, ответ: {response.text}")
                return {"chat_id": chat_id, "status": "error", "error": response.text}

        except Exception as e:
            logger.error(f"Ошибка при отправке файла {file_name} в чат {chat_id}: {type(e).__name__} — {e}")
            return {"chat_id": chat_id, "status": "error", "error": str(e)}

    def _send_single_message(
            self,
            chat_id: Union[int, str],
            message: str,
            start_time: float
    ) -> dict:
        """Отправляет сообщение в один чат."""
        try:
            response = requests.post(
                url=f"{self.telegram_domain}/bot{self.bot_token}/sendMessage",
                data={"chat_id": chat_id, "text": message},
                timeout=self.request_timeout
            )

            duration = time.time() - start_time
            if response.status_code == 200:
                logger.info(f"Сообщение успешно отправлено в чат {chat_id} за {duration:.2f} сек.")
                return {"chat_id": chat_id, "status": "success", "response": response.json()}
            else:
                logger.error(f"Ошибка отправки сообщения в чат {chat_id}: "
                             f"HTTP {response.status_code}, ответ: {response.text}")
                return {"chat_id": chat_id, "status": "error", "error": response.text}

        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения в чат {chat_id}: {type(e).__name__} — {e}")
            return {"chat_id": chat_id, "status": "error", "error": str(e)}

    @staticmethod
    def _normalize_chat_ids(chat_ids: Union[int, str, List, Tuple]) -> List:
        """Преобразует chat_ids в список."""
        if isinstance(chat_ids, (list, tuple)):
            return list(chat_ids)
        return [chat_ids]


if __name__ == '__main__':
    client = TelegramClient(
        bot_token="YOUR BOT TOKEN HERE",
        chat_ids=[123456789, 123456780]
    )

    client.send_message("Тестовое сообщение от нового клиента")

    client.send_file(__file__, caption="Тестовый файл")

    client.send_message(
        "Сообщение только для одного чата",
        chat_ids=123456789
    )
