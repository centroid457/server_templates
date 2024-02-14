import time
from typing import *
import requests
from PyQt5.QtCore import QThread
from collections import deque

from object_info import ObjectInfo


# =====================================================================================================================
Type_Response = Union[None, requests.Response, requests.ConnectTimeout]
Type_RequestBody = Union[str, dict]


# =====================================================================================================================
class UrlCreator:
    # SETTINGS -------------------------------------
    PROTOCOL: str = "http"
    HOST: str = "localhost"
    PORT: int = 80
    ROUTE: str = "stop123"

    def URL_create(
            self,
            host: Optional[str] = None,
            port: Optional[int] = None,
            route: Optional[str] = None,
    ) -> str:
        if host is None:
            host = self.HOST
        if port is None:
            port = self.PORT
        if route is None:
            route = self.ROUTE

        url = f"{self.PROTOCOL}://{host}:{port}/{route}"
        return url


class RequestItem(UrlCreator, QThread):
    """
    now its only POST!
    """
    # SETTINGS -------------------------------------
    START_ON_INIT: bool = None
    TIMEOUT_SEND: float = 1

    RETRY_LIMIT: int = 2
    RETRY_TIMEOUT: float = 0.5

    # AUX ------------------------------------------
    BODY: Type_RequestBody
    # REQUEST: Optional[requests.Request] = None
    RESPONSE: Optional[requests.Response] = None
    EXX_TIMEOUT: Union[None, requests.ConnectTimeout, Exception] = None
    attempt_all: int
    attempt_circle: int
    index: int = 0
    TIMESTAMP: float

    def __init__(self, body: Type_RequestBody):
        super().__init__()
        self.__class__.index += 1
        self.BODY = body
        self.attempt_all = 0
        self.attempt_circle = 0
        self.index = int(self.__class__.index)
        self.TIMESTAMP = time.time()

        if self.START_ON_INIT:
            self.start()

    def check_success(self) -> bool:
        result = self.RESPONSE is not None and self.RESPONSE.ok
        return result

    def __str__(self) -> str:
        return f"[{self.index=}/{self.attempt_all=}/{self.attempt_circle=}/{self.check_success()=}]{self.EXX_TIMEOUT=}/{self.RESPONSE=}"

    def __repr__(self) -> str:
        return str(self)

    def run(self):
        self.attempt_circle = 0

        url = self.URL_create()

        while self.attempt_circle == 0 or self.attempt_circle < self.RETRY_LIMIT:
            self.attempt_circle += 1
            self.attempt_all += 1

            with requests.Session() as session:
                try:
                    response = session.post(url=url, data=self.BODY, timeout=self.TIMEOUT_SEND)
                    self.RESPONSE = response
                except Exception as exx:
                    self.EXX_TIMEOUT = exx

            print(self)
            if self.check_success():
                break


# =====================================================================================================================
class HttpClientStack(QThread):
    # TODO: add timestamp
    # TODO: save send data

    # SETTINGS -------------------------------------
    REQUEST_CLS: Type[RequestItem] = RequestItem

    # AUX ------------------------------------------
    __stack: deque
    request_last: Optional[RequestItem] = None

    def __init__(self):
        super().__init__()
        self.__class__.__stack = deque()

    @classmethod
    @property
    def STACK(cls) -> deque:
        return cls.__stack

    # ------------------------------------------------------------------------------------------------
    def start(self, *args):
        """
        apply only one thread at once (from stack)!
        """
        if not self.isRunning():
            super().start(*args)

    # ------------------------------------------------------------------------------------------------
    def run(self):
        stack_attempt = 0
        while len(self.STACK):
            stack_attempt += 1

            # NEXT -----------------------------------------
            # change last
            if self.request_last is None or self.request_last.check_success():
                stack_attempt = 0
                self.request_last = self.STACK[0]

                if self.request_last.check_success():
                    self.STACK.popleft()
                continue

            # WORK -----------------------------------------
            print()
            print(f"{stack_attempt=}")
            print(f"len={len(self.STACK)}")
            self.request_last.run()

            if self.request_last.check_success():
                self.STACK.popleft()
                continue

            print(f"len={len(self.STACK)}/{self.STACK=}")
            if stack_attempt == 2:
                break
            else:
                time.sleep(1)

    def post(self, body: Optional[dict] = None):
        # TODO: add locker???
        body = body or {}
        item = self.REQUEST_CLS(body)
        self.STACK.append(item)
        # print(f"len={len(self.STACK)}")
        self.start()


# =====================================================================================================================
