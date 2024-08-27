import time
import keyboard
import threading

from logger.logger import Logger

from settings import selectors as se
from settings import settings
from util import decorators
from util.utils import path, wait

from humancursor import WebCursor
from seleniumbase import Driver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionBuilder

from seleniumbase.undetected.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

logger = Logger('Control')
logger.debug("Control Initialized Successfully.")


class SeleniumbaseTemplate:
    def __init__(self, user_data_dir_path: str, proxy: str = None) -> None:
        self.stop_listeners: bool = False
        self.logger = Logger('SeleniumbaseTemplate')
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
        threading.Thread(target=self.listener, args=('ctrl+esc', )).start()

        self.logger.debug('SeleniumbaseTemplate initialized successfully.')

    def listener(self, button: str) -> None:
        """
        keyboard listener to do an action if button was clicked.
        :param button: keyboard button to click
        """
        while not self.stop_listeners:
            if keyboard.is_pressed(button):
                match button:
                    case 'ctrl+m': pass  # add an event here
                    case 'ctrl+n': pass  # add an event here
                    case 'ctrl+esc':
                        self.driver.close()
                        self.driver.quit()
                        self.stop_listeners = True
                        return
            time.sleep(.05)

    @decorators.retry
    def find_element(self, selector: tuple[str, str], timeout: int = 20) -> WebElement:
        """
        wait til an element is on the browser page element.

        :param selector: selector or element to click
        :param timeout: timeout in seconds

        :rtype: WebElement
        :return: the element after finding it or False if not found after 5 retries
        """
        if isinstance(selector, WebElement):
            return selector
        else:
            return WebDriverWait(self.driver, timeout).until(
                ec.presence_of_element_located(selector)
            )

    @decorators.retry
    def click(self, element: tuple[str, str] | WebElement, timeout: int = 20) -> bool:
        """
        click on an element with WebCursor.

        :param element: selector or element to click
        :param timeout: timeout in seconds

        :rtype: bool
        :return: True if action finished successfully else False
        """
        cursor = WebCursor(self.driver)
        if isinstance(element, WebElement):
            element = element
        else:
            element = WebDriverWait(self.driver, timeout).until(
                ec.element_to_be_clickable(
                    self.find_element(element)
                )
            )

        cursor.move_to(element)
        cursor.click()

        return True

    @decorators.catch_exceptions
    def enter_keys(self, text: str, element: tuple[str, str] | WebElement, timeout: int = 20) -> bool:
        """
        write with keyboard actions.

        :param text: text to write
        :param element: selector or element to click
        :param timeout: timeout in seconds

        :rtype: bool
        :return: True if action finished successfully else False
        """
        if isinstance(element, tuple):
            element = WebDriverWait(self.driver, timeout).until(
                ec.element_to_be_clickable(
                    self.find_element(self.driver.find_elements(*element)[-1] or element)
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
            wait(1)
            chain.key_action.key_up(letter)
            chain.perform()

        return True

    def search_term(self, term_to_search: str, site_to_click: str, interval: int = 5) -> bool:
        """
        search a term on www.google.com and click on the relevant result.

        :param term_to_search: term to search
        :param site_to_click: site to click on
        :param interval: interval between clicks in seconds

        :rtype: bool
        :return: True if action finished successfully else False
        """
        # self.driver.get('https://www.google.com/')
        raise NotImplementedError('still on progress...')

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.driver.close()
        self.driver.quit()

        logger.exception(f'closed on an exception:\n {exc_type} \n {exc_val} \n {exc_tb}\n\n')
