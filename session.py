import time

from requests import Response
from curl_cffi.requests import Session as RequestsSession
import logging

from logger.logger import Logger
from util.decorators import retry


class Session(RequestsSession):
    def __init__(
            self,
            user_agent: str = "Mozilla/5 (Windows NT 10; Win64; x64) AppleWebKit/537 (KHTML, like Gecko)",
            proxy: str = None,
    ) -> None:
        """ a custom session class that handles retrying and proxy settings and fingerprints. """
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
        response = super(Session, self).get(timeout=20, impersonate="chrome110", *args, **kwargs)
        if not response:
            self.logger.error('GET request failure')
            return Response()
        return response

    @retry
    def post(self, *args, **kwargs) -> Response:
        """ POST request with retry decorator """
        time.sleep(1)
        response = super(Session, self).post(timeout=20, impersonate="chrome110", *args, **kwargs)
        if not response:
            self.logger.error('POST request failure')
            return Response()
        return response
