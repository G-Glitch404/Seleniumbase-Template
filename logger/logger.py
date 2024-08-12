import logging
from util.utils import path


class Color:
    """ Colors for loggers messages """
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'


class Logger(logging.LoggerAdapter):
    def __init__(self, logger, extra: dict = None):
        super().__init__(logger, extra)
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - [%(name)s] - %(levelname)s - %(threadName)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(
                    filename=path(f"logs//logger.log"),
                    mode="a",
                    delay=True,
                    encoding="utf-8",
                    errors="ignore",
                ),
            ],
        )

    def debug(self, msg, *args, **kwargs):
        """Delegate a debug call to the underlying logger."""
        msg = f"{Color.OKCYAN} {msg} {Color.ENDC}"
        self.log(logging.DEBUG, msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        """Delegate an info call to the underlying logger."""
        msg = f"{Color.OKGREEN} {msg} {Color.ENDC}"
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

    def log(self, level, msg, *args, **kwargs):
        """ Delegate a log call to the underlying logger, after adding contextual information from this adapter instance. """
        if self.isEnabledFor(level):
            msg, kwargs = self.process(msg, kwargs)
            self.logger.log(level, msg, *args, **kwargs)
