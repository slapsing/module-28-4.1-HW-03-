import logging
from django.core.management.base import BaseCommand

logger = logging.getLogger("django")
request_logger = logging.getLogger("django.request")
server_logger = logging.getLogger("django.server")
template_logger = logging.getLogger("django.template")
db_logger = logging.getLogger("django.db.backends")
security_logger = logging.getLogger("django.security")


class Command(BaseCommand):
    help = "Тестирование системы логирования (все уровни + email)."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(" Тестируем систему логирования..."))

        logger.debug("DEBUG сообщение (console only, если DEBUG=True).")
        logger.info("INFO сообщение (general.log при DEBUG=False).")
        logger.warning("WARNING сообщение (console/general.log).")

        try:
            1 / 0
        except ZeroDivisionError:
            request_logger.error("Ошибка в django.request (деление на ноль).", exc_info=True)
            server_logger.error("Ошибка в django.server (деление на ноль).", exc_info=True)
            template_logger.error("Ошибка в django.template (деление на ноль).", exc_info=True)
            db_logger.error("Ошибка в django.db.backends (деление на ноль).", exc_info=True)

        logger.critical("CRITICAL сообщение из django.")

        security_logger.warning("Подозрительная активность: попытка XSS-атаки.")

        self.stdout.write(self.style.SUCCESS(" Логирование протестировано."))
