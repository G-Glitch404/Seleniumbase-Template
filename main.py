import time
import random
import logging
import keyboard
import threading

from logger.logger import Logger

from settings import selectors as se
from settings import settings
from util import decorators
from util.utils import path

from humancursor import WebCursor
from seleniumbase import Driver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionBuilder

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebElement

logger = Logger(logging.getLogger('Control'), {})
for log in [
    "Control",
    "Session",
    "ExceptionsHandler",
    "Retry"]:
    logging.getLogger(log).setLevel(settings["DEBUGGING_LEVEL"])
logger.debug("Control Initialized Successfully.")


class SeleniumbaseTemplate:
    def __init__(self, user_data_dir_path: str, proxy: str = None) -> None:
        self.logger = Logger(logging.getLogger('SeleniumbaseTemplate'), {})
        self.driver = Driver(
            uc=True,
            undetectable=True,
            undetected=True,
            proxy=proxy,
            browser='chrome',
            disable_gpu=True,
            dark_mode=True,
            guest_mode=True,
            no_sandbox=True,
            do_not_track=True,
            user_data_dir=user_data_dir_path,
        )
        threading.Thread(target=self.__listen, args=('ctrl+esc', )).start()
        self.logger.debug('SeleniumbaseTemplate initialized successfully.')

    def __listen(self, btn: str):
        while True:
            if keyboard.is_pressed(btn):
                match btn:
                    case 'ctrl+m': pass  # add an event here
                    case 'ctrl+n': pass  # add an event here
                    case 'ctrl+esc':
                        self.driver.close()
                        self.driver.quit()
            time.sleep(0.1)

    @decorators.retry
    def __find_element(self, selector: tuple[str, str], timeout: int = 20) -> WebElement:
        """ find an element with WebCursor """
        return WebDriverWait(self.driver, timeout).until(
            ec.presence_of_element_located(selector)
        )

    @decorators.retry
    def __click(self, element: tuple[str, str] | WebElement, timeout: int = 20) -> bool:
        """ click on an element with WebCursor """
        cursor = WebCursor(self.driver)
        if isinstance(element, WebElement):
            element = element
        else:
            element = WebDriverWait(self.driver, timeout).until(
                ec.element_to_be_clickable(
                    self.__find_element(element)
                )
            )

        cursor.move_to(element)
        cursor.click()

        return True

    @decorators.catch_exceptions
    def __enter_keys(self, text: str, element: tuple[str, str] | WebElement, timeout: int = 20) -> bool:
        """ write with keyboard actions """
        if isinstance(element, tuple):
            element = WebDriverWait(self.driver, timeout).until(
                ec.element_to_be_clickable(
                    self.__find_element(self.driver.find_elements(*element)[-1] or element)
                )
            )
        else: element = element
        element.send_keys(Keys.CONTROL + 'a' + Keys.DELETE)

        cursor = WebCursor(self.driver)
        chain = ActionBuilder(self.driver, duration=250)

        cursor.move_to(element)
        cursor.click()

        for letter in text:
            chain.key_action.key_down(letter)
            chain.perform()

            self.driver.sleep(random.choice([random.uniform(.01, .1)]) for _ in range(35))

            chain.key_action.key_up(letter)
            chain.perform()

        return True

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.driver.close()
        self.driver.quit()

        logger.debug(f'user_data_dir generator closed on an exception:\n {exc_type} \n {exc_val} \n {exc_tb}\n\n')
