from scraping_tools.telegram_tools import send_telegram_log, send_file_result


class LoggingMixin:
    def engine_started(self):
        if self.production:
            send_telegram_log(message="-" * 10 + "STARTED" + "-" * 10)
            send_telegram_log(f"engine_started {self.name} \n(ссылки: {self.start_url})")
        print(f"<<< engine_started {self.name} >>> ")
        # spider.logger.info(f"<<< engine_started >>> {spider.name}")

    def spider_error(self, spider):
        if self.production:
            send_telegram_log(f"spider_error {self.name}")
            send_file_result(self.log_file, caption="Логи")
            send_telegram_log(message="-" * 10 + "ERROR" + "-" * 10)
        spider.logger.info(f"<<< spider_error {self.name} >>>")

    def spider_closed(self, spider, reason):
        if self.production:
            send_telegram_log(f"spider_closed {self.name} {reason}")
        spider.logger.info(f"<<< spider_closed {self.name} {reason} >>>")

    def feed_exporter_closed(self):
        if self.production:
            send_file_result(self.results_file_path)
            send_telegram_log(message=f"feed_exporter_closed {self.name}")
        print(f"<<< feed_exporter_closed {self.name} >>> ")
        # ShopPuntoluceSpiderSpider.logger.info(f"<<< Spider feed_exporter_closed signal >>> {ShopPuntoluceSpiderSpider.name}")

    def engine_stopped(self):
        if self.production:
            send_telegram_log(f"engine_stopped {self.name}")
            send_file_result(self.log_file, caption="Логи")
            send_telegram_log(message="-" * 10 + "ENGINE STOPED" + "-" * 10)
        print(f"<<< engine_stopped {self.name} >>> ")
        # spider.logger.info(f"<<< engine_stopped {spider.name} >>>")