import time
from typing import *
import requests
from PyQt5.QtCore import QThread
from collections import deque
from enum import Enum, auto

from object_info import ObjectInfo

from server_templates.url import UrlCreator


# =====================================================================================================================
Type__Response = Union[None, requests.Response, requests.ConnectTimeout]
Type__RequestBody = Union[str, dict]


class ResponseMethod(Enum):
    POST = auto()
    GET = auto()


# =====================================================================================================================
class Client_RequestItem(UrlCreator, QThread):
    """
    DONT USE IT AS ONE INSTANCE FOR SEVERAL REQUESTS!!!
    You need keep it only to manage results or sent in further time!

    So Only ONE REQUESTITEM FOR ONE Request!

    create object and wait result by wait() or connect slot finished
    """
    # SETTINGS -------------------------------------
    START_ON_INIT: bool = None      # DONT DELETE!!! useful for delayed/pending requests
    TIMEOUT_SEND: float = 1

    RETRY_LIMIT: int = 1
    RETRY_TIMEOUT: float = 0.5
    RETRY_COUNT: int

    METHOD: ResponseMethod = ResponseMethod.POST

    # AUX ------------------------------------------
    BODY: Optional[Type__RequestBody] = None
    # REQUEST: Optional[requests.Request] = None
    RESPONSE: Optional[requests.Response] = None
    EXCEPTION: Union[None, requests.ConnectTimeout, Exception] = None

    attempt_all: int
    INDEX: int = 0
    TIMESTAMP: float

    def __init__(
            self,
            body: Optional[Type__RequestBody] = None,
            method: Optional[ResponseMethod] = None,

            # url: Optional[str] = None,
            host: Optional[str] = None,
            port: Optional[int] = None,
            route: Optional[str] = None,
    ):
        super().__init__()

        if body is not None:
            self.BODY = body
        if method is not None:
            self.METHOD = method

        # if url is None:
        #     url = self.HOST
        if host is not None:
            self.HOST = host
        if port is not None:
            self.PORT = port
        if route is not None:
            self.ROUTE = route

        self.__class__.INDEX += 1
        self.INDEX = int(self.__class__.INDEX)
        self.attempt_all = 0
        self.RETRY_COUNT = 0
        self.TIMESTAMP = time.time()

        if self.START_ON_INIT:
            self.start()

    def check_success(self) -> bool:
        result = False
        if self.RESPONSE is not None:
            result = self.RESPONSE.ok
        return result

    def __str__(self) -> str:
        return f"[{self.INDEX=}/{self.attempt_all=}/{self.RETRY_COUNT=}/{self.check_success()=}]{self.EXCEPTION=}/{self.RESPONSE=}"

    def __repr__(self) -> str:
        return str(self)

    def run(self) -> None:
        self.RETRY_COUNT = 0

        url = self.URL_create()

        while self.RETRY_COUNT == 0 or self.RETRY_COUNT < self.RETRY_LIMIT:
            self.RETRY_COUNT += 1
            self.attempt_all += 1

            self.RESPONSE = None
            self.EXCEPTION = None

            with requests.Session() as session:
                try:
                    if self.METHOD == ResponseMethod.POST:
                        self.RESPONSE = session.post(url=url, json=self.BODY or {}, timeout=self.TIMEOUT_SEND)
                    elif self.METHOD == ResponseMethod.GET:
                        self.RESPONSE = session.get(url=url, timeout=self.TIMEOUT_SEND)
                except Exception as exx:
                    self.EXCEPTION = exx

            print(self)
            if self.check_success():
                break

    # ---------------------------------------------------------------
    # DONT USE anything LIKE THIS BELOW!!!
    # def start(self, *args):
    #     if not self.isRunning():
    #         super().start(*args)

    # def post(self, url=None, body=None):
    #     self.start()

    # def get(self, url=None):  #????
    #     self.start()


# =====================================================================================================================
class Client_RequestsStack(QThread):
    # TODO: save send data

    # SETTINGS -------------------------------------
    REQUEST_CLS: Type[Client_RequestItem] = Client_RequestItem
    ATTEMPT_SEND_LIMIT: int = 1

    # AUX ------------------------------------------
    __stack: deque
    request_last: Optional[Client_RequestItem] = None

    def __init__(self, request_cls: Optional[Type[REQUEST_CLS]] = None):
        super().__init__()
        if request_cls is not None:
            self.REQUEST_CLS = request_cls

        self.__stack = deque()

    @property
    def stack(self) -> deque:
        return self.__stack

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
        while len(self.stack):
            stack_attempt += 1

            # NEXT -----------------------------------------
            # change last
            if self.request_last is None or self.request_last.check_success():
                stack_attempt = 0
                self.request_last = self.stack[0]

                if self.request_last.check_success():
                    self.stack.popleft()
                continue

            # WORK -----------------------------------------
            print()
            print(f"{stack_attempt=}")
            print(f"len={len(self.stack)}")
            self.request_last.run()

            if self.request_last.check_success():
                self.stack.popleft()
                continue

            print(f"len={len(self.stack)}/{self.stack=}")
            if stack_attempt == self.ATTEMPT_SEND_LIMIT:
                break
            else:
                time.sleep(1)

        if len(self.stack):
            print(f"[WARN] stack is stopped by some errors")
        else:
            print(f"[OK] stack is empty")

    def send(self, **kwargs) -> None:    # maybe rename to SEND???
        """
        work usually with POST
        """
        # TODO: add locker???
        item = self.REQUEST_CLS(**kwargs)
        self.stack.append(item)
        self.start()

    def check_success(self) -> bool:
        result = len(self.stack) == 0 and self.request_last.check_success()
        return result


# =====================================================================================================================
