import json
import time
import logging

from logger.logger import Logger
from functools import wraps
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
    ElementNotInteractableException,
)

catch_logger = Logger('ExceptionsHandler')
retry_logger = Logger('Retry')
__exceptions = (
    Exception,
    json.decoder.JSONDecodeError,
    NoSuchElementException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
    ElementNotInteractableException,
    TimeoutException,
)


def retry(func, retries: int = 5, interval: int = 1, exceptions: tuple = __exceptions):
    """ decorator for retrying a function if an exception occurs after interval seconds """
    @wraps(func)
    def wrapper(*args, **kwargs):
        for _ in range(retries):
            try: return func(*args, **kwargs)
            except exceptions as e:
                retry_logger.exception(f'function {func.__name__} with args {args, kwargs} failed with exception {e} retrying after interval...')
            finally: time.sleep(interval)
        retry_logger.exception(f'function {func.__name__} with args {args, kwargs} failed to execute.')
        return False

    return wrapper


def catch_exceptions(func, exceptions: tuple = __exceptions):
    """ decorator for catching selenium exceptions """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try: return func(*args, **kwargs)
        except exceptions as e:
            catch_logger.exception(f'function {func.__name__} with parameters: {args, kwargs} failed with exception {e}')
            return False

    return wrapper
