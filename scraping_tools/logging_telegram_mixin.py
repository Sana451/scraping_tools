from scraping_tools.telegram_tools import send_telegram_log, send_file_result


class LoggingTelegramMixin:
    MSG_ENGINE_STARTED = "<<< engine_started {name} \n ссылки: {links}>>>"
    MSG_ENGINE_STOPPED = "<<< engine_stopped {name} >>>"
    MSG_SPIDER_ERROR = "<<< spider_error {name} >>>"
    MSG_SPIDER_CLOSED = "<<< spider_closed {name} {reason} >>>"
    MSG_FEED_EXPORTER_CLOSED = "<<< feed_exporter_closed {name} >>>"
    MSG_PROGRESS_UPDATE = "<<< Обработано {current}/{total} страниц >>>"

    def get_safe(self, attr_name, default=None):
        return getattr(self, attr_name, default)

    def engine_started(self):
        message = self.MSG_ENGINE_STARTED.format(
            name=self.get_safe("name", "unknown"),
            links=self.get_safe('start_url', 'not implemented')
        )
        print(message)
        if self.get_safe("production", False):
            send_telegram_log(message)

    def spider_error(self, spider):
        message = self.MSG_SPIDER_ERROR.format(name=self.get_safe("name", "unknown"))
        spider.logger.info(message)
        print(message)
        if self.get_safe("production", False):
            send_telegram_log(message)
            send_file_result(self.get_safe("log_file"), caption="Логи")

    def spider_closed(self, spider, reason):
        message = self.MSG_SPIDER_CLOSED.format(name=self.get_safe("name", "unknown"), reason=reason)
        spider.logger.info(message)
        print(message)
        if self.get_safe("production", False):
            send_telegram_log(message)
            send_file_result(self.get_safe("results_file_path"), caption="результаты")

    def feed_exporter_closed(self):
        message = self.MSG_FEED_EXPORTER_CLOSED.format(name=self.get_safe("name", "unknown"))
        print(message)
        if self.get_safe("production", False):
            send_file_result(self.get_safe("results_file_path"), caption="результаты")
            send_telegram_log(message)

    def engine_stopped(self):
        message = self.MSG_ENGINE_STOPPED.format(name=self.get_safe("name", "unknown"))
        print(message)
        if self.get_safe("production", False):
            send_telegram_log(message)
            send_file_result(file_name=self.get_safe("log_file"), caption=f"Логи")
            send_file_result(self.get_safe("results_file_path"), caption="результаты")

    def track_progress_for_telegram(self, progress, total):
        progress_checkpoints = self.get_safe("progress_checkpoints", [1, 5, 10, 100, 1000])
        sent_progress_checkpoints = self.get_safe("sent_progress_checkpoints")
        if progress in progress_checkpoints and progress not in sent_progress_checkpoints:
            sent_progress_checkpoints.add(progress)
            message = self.MSG_PROGRESS_UPDATE.format(current=progress, total=total)
            print(message)
            if self.get_safe("production", False):
                send_telegram_log(message)
                send_file_result(file_name=self.get_safe("log_file"), caption=f"Логи")
                send_file_result(self.get_safe("results_file_path"), caption="Промежуточные результаты")
