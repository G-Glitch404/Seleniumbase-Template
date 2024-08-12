import time

from requests import Response
from curl_cffi.requests import Session as RequestsSession
import logging

from logger.logger import Logger
from util.decorators import retry


class Session(RequestsSession):
    def __init__(self, proxy: str = None, user_agent: str = None) -> None:
        super(Session, self).__init__()
        self.logger = Logger(logging.getLogger('Session'), {})

        if user_agent: self.headers.update({"User-Agent": user_agent})
        self.get('https://www.google.com/')  # we add some cookies so the session is not empty
        if proxy: self.proxies = {"https": proxy, "http": proxy}  # then we add the proxies after so we save bandwidth

        self.logger.debug('Session initialized successfully')

    @retry
    def get(self, *args, **kwargs) -> Response:
        """ GET request with retry decorator """
        time.sleep(1)
        response = super(Session, self).get(
            headers=self.headers, cookies=self.cookies,
            timeout=10, impersonate="chrome110", *args, **kwargs
        )
        if not response:
            self.logger.error('GET request failure')
            return Response()
        return response

    @retry
    def post(self, *args, **kwargs) -> Response:
        """ POST request with retry decorator """
        time.sleep(1)
        response = super(Session, self).post(
            headers=self.headers, cookies=self.cookies,
            timeout=10, impersonate="chrome110", *args, **kwargs
        )
        if not response:
            self.logger.error('POST request failure')
            return Response()
        return response
