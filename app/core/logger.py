import logging
import sys
import os

from core.config import settings


class LoggerAPI:
    def __init__(self):
        self._console_handler()
        self._file_handler()

    def _console_handler(self):
        self.console_logger = logging.getLogger('console')
        self.console_logger.setLevel(logging.DEBUG)
        self.console_logger.propagate = False

        fmt = logging.Formatter('[CONSOLE - %(filename)s] %(asctime)s | %(levelname)s | %(message)s', '%H:%M:%S')
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(fmt=fmt)

        self.console_logger.addHandler(handler)

    def _file_handler(self):
        self.file_logger = logging.getLogger('file')
        self.file_logger.setLevel(logging.WARNING)
        self.file_logger.propagate = False

        fmt = logging.Formatter('[FILE - %(filename)s] %(asctime)s | %(levelname)s | %(message)s', '%H:%M:%S')
        handler = logging.FileHandler(
            filename=os.path.join(settings.BASE_DIR, 'loggers/api_logger.log'),
            mode='a',
            encoding='utf-8'
        )
        handler.setLevel(logging.WARNING)
        handler.setFormatter(fmt=fmt)

        self.file_logger.addHandler(handler)

    def debug_message(self, message: str):
        self.console_logger.debug(msg=message)

    def info_message(self, message: str):
        self.console_logger.info(msg=message)

    def warning_message(self, message: str):
        self.file_logger.warning(msg=message)

    def error_message(self, message: str):
        self.file_logger.error(msg=message)


logger = LoggerAPI()
