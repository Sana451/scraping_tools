# python
import os
import logging
import requests
import boto3
from botocore.exceptions import ClientError
from urllib.parse import urlparse
from typing import Optional, Dict

logger = logging.getLogger(__name__)

class DigitalOceanSpaceClient:
    def __init__(
        self,
        secret_key: str,
        access_key: str = "DO801ZEM3KU6BQ72WFPG",
        space_name: str = "famaga-crm",
        region_name: str = "fra1",
        base_folder: str = "famaga-crm",
        proxies: Optional[Dict[str, str]] = None,
    ):
        self.space_name = space_name
        self.region_name = region_name
        self.base_folder = base_folder.strip("/") if base_folder else ""
        self.proxies = proxies or self._get_proxies()

        if self.proxies:
            logger.debug("Using proxies: %s", {k: ("<hidden>" if "@" in v else v) for k, v in self.proxies.items()})
            for scheme in ("http", "https"):
                val = self.proxies.get(scheme)
                if val:
                    os.environ[f"{scheme.upper()}_PROXY"] = val
                    os.environ[f"{scheme.lower()}_proxy"] = val

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

    def _get_proxies(self) -> Optional[Dict[str, str]]:
        http = os.getenv("HTTP_PROXY") or os.getenv("http_proxy")
        https = os.getenv("HTTPS_PROXY") or os.getenv("https_proxy")
        if not http and not https:
            return None
        proxies = {}
        if http:
            proxies["http"] = http
        if https:
            proxies["https"] = https
        return proxies

    def _is_url(self, path: str) -> bool:
        parsed = urlparse(path)
        return parsed.scheme in ("http", "https")

    def _download_image(self, image_url: str, timeout: int = 10):
        try:
            response = requests.get(image_url, timeout=timeout, proxies=self.proxies)
            response.raise_for_status()

            content_type = response.headers.get("content-type", "")
            if not content_type.startswith("image/"):
                raise ValueError(f"Некорректный тип содержимого: {content_type}")

            return response.content, content_type

        except requests.exceptions.ProxyError as e:
            msg = str(e)
            logger.error("ProxyError при скачивании %s: %s", image_url, msg)
            if "407" in msg or "Proxy Authentication Required" in msg or "Tunnel connection failed: 407" in msg:
                raise RuntimeError(f"Ошибка авторизации прокси при скачивании изображения {image_url}: {msg}") from e
            raise RuntimeError(f"Прокси ошибка при скачивании изображения {image_url}: {msg}") from e

        except requests.exceptions.RequestException as e:
            logger.exception("RequestException при скачивании %s: %s", image_url, e)
            raise RuntimeError(f"Ошибка при скачивании изображения {image_url}: {e}") from e

        except Exception as e:
            logger.exception("Неожиданная ошибка при скачивании %s: %s", image_url, e)
            raise RuntimeError(f"Ошибка при скачивании изображения {image_url}: {e}") from e

    def _read_local_file(self, file_path: str):
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
            logger.error("Файл не найден: %s", file_path)
            raise RuntimeError(f"Файл не найден: {file_path}")

    def upload_image(self, source_path: str, s3_key: str) -> str:
        if not s3_key:
            raise ValueError("Параметр 's3_key' обязателен и не может быть пустым.")

        if self._is_url(source_path):
            image_bytes, content_type = self._download_image(source_path)
        else:
            image_bytes, content_type = self._read_local_file(source_path)

        key_path = f"{self.base_folder}/{s3_key}" if self.base_folder else s3_key

        try:
            self.s3_client.put_object(
                Bucket=self.space_name,
                Key=key_path,
                Body=image_bytes,
                ContentType=content_type,
                ACL="public-read",
            )

            public_url = (
                f"https://{self.space_name}.{self.region_name}.digitaloceanspaces.com/{key_path}"
            )

            logger.info("Загружено: %s", public_url)
            return public_url

        except ClientError as e:
            error_msg = e.response.get("Error", {}).get("Message", str(e))
            logger.error("ClientError при загрузке %s: %s", s3_key, error_msg)
            raise RuntimeError(f"Ошибка при загрузке {s3_key} в Space: {error_msg}") from e

        except Exception as e:
            msg = str(e)
            logger.exception("Ошибка при загрузке %s: %s", s3_key, msg)
            if "407" in msg or "Proxy Authentication Required" in msg:
                raise RuntimeError(f"Ошибка авторизации прокси при загрузке {s3_key}: {msg}") from e
            raise RuntimeError(f"Не удалось загрузить {s3_key}: {msg}") from e


if __name__ == "__main__":
    # Пример запуска: логирование в консоль
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    from dotenv import load_dotenv
    load_dotenv(dotenv_path="/home/sana451/PycharmProjects/scrapy_parsers/.env")

    proxies = {
        "http": "http://U9xafG:ga5jh6@186.65.118.126:9983",
        "https": "http://U9xafG:ga5jh6@186.65.118.126:9983",
    }
    try:

        resp = requests.get("https://api.ipify.org?format=json", proxies=proxies, timeout=5)
        resp.raise_for_status()
        print("Внешний IP:", resp.json().get("ip"))
    except Exception as e:
        logger.error("Не удалось получить внешний IP: %s", e)

    print(os.getenv("DIGITAL_OCEAN_SECRET_KEY"))

    client = DigitalOceanSpaceClient(
        secret_key=os.getenv("DIGITAL_OCEAN_SECRET_KEY", ""),
        proxies=proxies,
    )

    image_url = "https://shop.kaeltefischer.de/media/GR8/RESU01/8505160-8505161.jpg"
    try:
        public_link = client.upload_image(image_url, s3_key="HRN-44N.png")
        print("Публичная ссылка:", public_link)
    except Exception as e:
        logger.error("Загрузка не выполнена: %s", e)