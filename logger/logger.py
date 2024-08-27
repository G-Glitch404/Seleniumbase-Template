import logging
import os.path
import sys

from logging.handlers import RotatingFileHandler
from logging import LogRecord

from util.utils import path

class Color:
    """ Colors for loggers messages """
    BLACK = '\033[30m'
    LIGHTBLACK_EX = '\033[90m'
    BLUE = '\033[34m'
    LIGHTBLUE_EX = '\033[94m'
    MAGENTA = '\033[35m'
    DEBUG = '\033[96m'
    SUCCESS = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'


class Logger(logging.LoggerAdapter):
    def __init__(
        self,
        logger_name: str = "Logger",
        logs_folder: str = "logs",
        create_file: bool = True,
        propagate_logging: bool = True,
        extra: dict = None,
    ) -> None:
        """ a better and more advanced logging adapter. """
        os.makedirs(
            name=path(logs_folder),
            exist_ok=True
        )  # creating and adding defaults
        self.logs_file_path = path(logs_folder, f"{logger_name}.log")

        self.extra = extra or {}
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = propagate_logging

        self.logging_formatter = logging.Formatter(
            fmt=self.__create_fmt_message(),
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        if propagate_logging: self.logger.addHandler(self.setup_stream_handler())
        if create_file: self.logger.addHandler(self.setup_file_handler())

        super(Logger, self).__init__(self.logger, self.extra)

    def setup_stream_handler(self) -> logging.StreamHandler:
        stream_handler = logging.StreamHandler(sys.stderr)

        stream_handler.setLevel(settings['LOGGING_LEVEL'])
        stream_handler.setFormatter(self.logging_formatter)

        return stream_handler

    def setup_file_handler(self) -> RotatingFileHandler:
        """ setup a file handler for each Logger. """
        def filter_fmt_msg(msg: str) -> str:
            for color in Color.__dict__.values():
                if not  isinstance(color, str): continue
                msg = msg.replace(color, '').strip()
            return msg

        file_handler = RotatingFileHandler(
            filename=self.logs_file_path,
            mode='a',
            encoding='utf-8',
            maxBytes=1048576 * 50,  # log file size of 50MB
            backupCount=0,
            delay=True,
        )

        file_handler.setLevel(settings['LOGGING_LEVEL'])
        file_handler.addFilter(self.filter)
        file_handler.setFormatter(
            logging.Formatter(
                fmt=filter_fmt_msg(
                    self.__create_fmt_message()
                ),
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )

        return file_handler

    def __create_fmt_message(self) -> str:
        """ Add contextual information from this adapter to the log record. """
        fmt: str = f"{Color.LIGHTBLUE_EX}%(asctime)s   {Color.BLUE}[%(name)s]   {Color.MAGENTA}%(levelname)s: %(levelno)s{Color.LIGHTBLACK_EX}"
        if self.extra:
            for key in self.extra.keys():
                fmt += f"  -  [{key}: %({key})s]"
        return fmt + f":{Color.ENDC} %(message)s "

    @staticmethod
    def filter(record: LogRecord) -> bool:
        for k, v in record.__dict__.items():
            if not isinstance(v, str): continue
            for color in Color.__dict__.values():
                if not isinstance(color, str): continue
                record.__dict__[k] = record.__dict__[k].replace(color, '').strip()

        return True

    def log(self, level, msg, *args, **kwargs):
        """ Delegate a log call to the underlying logger, after adding contextual information from this adapter. """
        if self.isEnabledFor(level):
            msg, kwargs = self.process(msg, kwargs)
            self.logger.log(level, msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        """Delegate a debug call to the underlying logger."""
        msg = f"{Color.DEBUG} {msg} {Color.ENDC}"
        self.log(logging.DEBUG, msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        """Delegate an info call to the underlying logger."""
        msg = f"{Color.SUCCESS} {msg} {Color.ENDC}"
        self.log(logging.INFO, msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """Delegate a warning call to the underlying logger."""
        msg = f"{Color.WARNING} {msg} {Color.ENDC}"
        self.log(logging.WARNING, msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """Delegate an error call to the underlying logger."""
        msg = f"{Color.FAIL} {msg} {Color.ENDC}"
        self.log(logging.ERROR, msg, *args, **kwargs)

    def exception(self, msg, *args, exc_info=False, **kwargs):
        """ Delegate an exception call to the underlying logger. """
        msg = f"{Color.BOLD + Color.FAIL} {msg} {Color.ENDC}"
        self.log(logging.ERROR, msg, *args, exc_info=exc_info, **kwargs)


if __name__ == '__main__':
    logger = Logger('LoggingTest', extra={"spam": "eggs"})

    logger.debug('debug')
    logger.info('info')
    logger.warning('warning')
    logger.error('error')
    logger.exception('exception')
