import time
from typing import Optional, Set, List, Any

from scraping_tools.telegram_client import TelegramClient


class LoggingTelegramMixin:
    name: str
    production: bool
    results_file_path: str
    log_file: str
    start_url: Optional[str]
    progress_checkpoints: List[int]
    sent_progress_checkpoints: Set[int]
    last_sent_time: float
    send_interval: int
    crawler: Any
    logger: Any
    telegram_client: TelegramClient

    MSG_ENGINE_STARTED = "Started Engine {name} \n {links}"
    MSG_ENGINE_STOPPED = "Stopped Engine \n {name}"
    MSG_SPIDER_ERROR = "Error \n {name}"
    MSG_SPIDER_CLOSED = "Closed {name} \n {reason}"
    MSG_FEED_EXPORTER_CLOSED = "Feed_exporter_closed \n {name}"
    MSG_PROGRESS_UPDATE = "{name} \n обработал {current}/{total} страниц"
    MSG_TIMEOUT_UPDATE = "{name} \n обработал {total_processed} страниц"

    def get_safe(self, attr_name, default=None):
        value = getattr(self, attr_name, default)
        return value

    def engine_started(self):
        name = self.get_safe("name", "unknown")
        links = self.get_safe('start_url', 'not implemented')
        message = self.MSG_ENGINE_STARTED.format(name=name, links=links)
        self.logger.info(f"Engine started with name: {name}, start_url: {links}")
        print(message)

        if self.get_safe("production", False):
            self.logger.info("Sending engine started message to Telegram")
            self.telegram_client.send_message(message)

    def spider_error(self, spider):
        name = self.get_safe("name")
        log_file = self.get_safe("log_file")
        message = self.MSG_SPIDER_ERROR.format(name=name)
        self.logger.warning(f"Spider error occurred: {message}")
        print(message)

        if self.get_safe("production", False):
            self.logger.info(f"Sending spider error to Telegram with log file: {log_file}")
            self.telegram_client.send_message(message)
            self.telegram_client.send_file(
                file_name=log_file,
                caption=f"Логи \n {name}"
            )

    def spider_closed(self, spider, reason):
        name = self.get_safe("name")
        results_file_path = self.get_safe("results_file_path")
        message = self.MSG_SPIDER_CLOSED.format(name=name, reason=reason)
        self.logger.info(f"Spider closed: {message}")
        self.logger.info(f"Sending spider closed message and results to Telegram. Results: {results_file_path}")
        self.telegram_client.send_message(message)
        self.telegram_client.send_file(
            file_name=results_file_path,
            caption=f"Результаты \n {name}"
        )

    def feed_exporter_closed(self):
        name = self.get_safe("name")
        results_file_path = self.get_safe("results_file_path")
        message = self.MSG_FEED_EXPORTER_CLOSED.format(name=name)
        self.logger.info(f"Feed exporter closed: {message}")
        self.logger.info(f"Sending feed exporter results to Telegram: {results_file_path}")
        self.telegram_client.send_message(message)
        self.telegram_client.send_file(
            file_name=results_file_path,
            caption=f"Результаты \n {name}"
        )

    def engine_stopped(self):
        name = self.get_safe("name")
        results_file_path = self.get_safe("results_file_path")
        log_file = self.get_safe("log_file")
        message = self.MSG_ENGINE_STOPPED.format(name=name)
        self.logger.info(f"Engine stopped: {message}")
        self.logger.info("Sending engine stopped message and final files to Telegram")
        self.telegram_client.send_message(message)
        self.telegram_client.send_file(
            file_name=results_file_path,
            caption=f"Результаты \n {name}"
        )
        self.telegram_client.send_file(
            file_name=log_file,
            caption=f"Логи \n {name}"
        )

    def track_progress_for_telegram(self, progress, total):
        name = self.get_safe('name')
        results_file_path = self.get_safe("results_file_path")
        log_file = self.get_safe("log_file")
        progress_checkpoints = self.get_safe("progress_checkpoints", [1, 5, 10, 100, 1000])
        sent_progress_checkpoints = self.get_safe("sent_progress_checkpoints")

        self.logger.debug(
            f"Progress: {progress}, Total: {total}, Checkpoints: {progress_checkpoints}, Sent: {sent_progress_checkpoints}")

        if progress in progress_checkpoints and progress not in sent_progress_checkpoints:
            sent_progress_checkpoints.add(progress)
            message = self.MSG_PROGRESS_UPDATE.format(name=name, current=progress, total=total)
            self.logger.info(f"Sending progress update: {message}")

            self.telegram_client.send_message(message)
            self.telegram_client.send_file(
                file_name=results_file_path,
                caption=f"Промежуточные результаты \n {name}"
            )
            self.telegram_client.send_file(
                file_name=log_file,
                caption=f"Логи \n {name}"
            )

    def send_updates_with_timeout(self):
        name = self.get_safe('name')
        results_file_path = self.get_safe("results_file_path")
        log_file = self.get_safe("log_file")
        last_sent_time = self.get_safe("last_sent_time")
        send_interval = self.get_safe("send_interval")

        current_time = time.time()
        total_processed = self.crawler.stats.get_value('scheduler/dequeued', 0)
        self.logger.debug(
            f"Timeout check for {name}: last_sent={last_sent_time}, now={current_time}, interval={send_interval}, processed={total_processed}")

        if send_interval and (current_time - last_sent_time >= send_interval):
            message = self.MSG_TIMEOUT_UPDATE.format(name=name, total_processed=total_processed)
            self.logger.info(f"Timeout reached, sending update: {message}")
            self.telegram_client.send_message(message)
            self.telegram_client.send_file(
                file_name=results_file_path,
                caption=f"Промежуточные результаты \n {name}"
            )
            self.telegram_client.send_file(
                file_name=log_file,
                caption=f"Логи \n {name}"
            )

            self.last_sent_time = current_time
