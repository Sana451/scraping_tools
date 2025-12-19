import os
import requests
import boto3
from botocore.exceptions import ClientError
from urllib.parse import urlparse


class DigitalOceanSpaceClient:
    def __init__(
        self,
        secret_key: str,
        access_key: str = "DO801ZEM3KU6BQ72WFPG",
        space_name: str = "famaga-crm",
        region_name: str = "fra1",
        base_folder: str = "famaga-crm",
    ):
        """
        Клиент для работы с DigitalOcean Spaces (аналог S3).
        """
        self.space_name = space_name
        self.region_name = region_name
        self.base_folder = base_folder.strip("/") if base_folder else ""

        self.s3_client = boto3.client(
            "s3",
            endpoint_url=f"https://{region_name}.digitaloceanspaces.com",
            region_name=region_name,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            config=boto3.session.Config(
                connect_timeout=5,
                read_timeout=5,
                retries={"max_attempts": 3},
            ),
        )

    def _is_url(self, path: str) -> bool:
        """Проверяет, является ли строка URL."""
        parsed = urlparse(path)
        return parsed.scheme in ("http", "https")

    def _download_image(self, image_url: str, timeout: int = 10):
        """Скачивает изображение по URL с таймаутом и обработкой ошибок."""
        try:
            response = requests.get(image_url, timeout=timeout)
            response.raise_for_status()

            content_type = response.headers.get("content-type", "")
            if not content_type.startswith("image/"):
                raise ValueError(f"Некорректный тип содержимого: {content_type}")

            return response.content, content_type

        except Exception as e:
            raise RuntimeError(f"Ошибка при скачивании изображения {image_url}: {e}")

    def _read_local_file(self, file_path: str):
        """Читает локальный файл и определяет content-type по расширению."""
        ext = os.path.splitext(file_path)[1].lower()
        content_types = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
            ".webp": "image/webp",
        }
        content_type = content_types.get(ext, "application/octet-stream")

        try:
            with open(file_path, "rb") as f:
                return f.read(), content_type
        except FileNotFoundError:
            raise RuntimeError(f"Файл не найден: {file_path}")

    # --- Основная логика загрузки ---
    def upload_image(self, source_path: str, s3_key: str) -> str:
        """
        Загружает изображение (по URL или локальному пути) в Space.
        Возвращает публичный URL.
        """
        if not s3_key:
            raise ValueError("Параметр 's3_key' обязателен и не может быть пустым.")

        # Определяем источник (URL или файл)
        if self._is_url(source_path):
            image_bytes, content_type = self._download_image(source_path)
        else:
            image_bytes, content_type = self._read_local_file(source_path)

        # Формируем путь внутри бакета
        key_path = f"{self.base_folder}/{s3_key}" if self.base_folder else s3_key

        try:
            self.s3_client.put_object(
                Bucket=self.space_name,
                Key=key_path,
                Body=image_bytes,
                ContentType=content_type,
                ACL="public-read",  # обязательно, иначе файл не откроется по URL
            )

            public_url = (
                f"https://{self.space_name}.{self.region_name}.digitaloceanspaces.com/{key_path}"
            )

            print(f"Загружено: {public_url}")
            return public_url

        except ClientError as e:
            error_msg = e.response["Error"]["Message"]
            raise RuntimeError(f"Ошибка при загрузке {s3_key} в Space: {error_msg}")


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv(dotenv_path="/home/sana451/PycharmProjects/scrapy_parsers/.env")

    print(os.getenv("DIGITAL_OCEAN_SECRET_KEY"))

    client = DigitalOceanSpaceClient(
        secret_key=os.getenv("DIGITAL_OCEAN_SECRET_KEY", ""),
    )

    image_url = "https://shop.kaeltefischer.de/media/GR8/RESU01/8505160-8505161.jpg"
    public_link = client.upload_image(image_url, s3_key="HRN-44N.png")

    print("Публичная ссылка:", public_link)
