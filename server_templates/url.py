import time
from typing import *
import requests
from PyQt5.QtCore import QThread
from collections import deque
from enum import Enum, auto

from object_info import ObjectInfo


# =====================================================================================================================
class UrlCreator:
    # SETTINGS -------------------------------------
    PROTOCOL: Optional[str] = None
    HOST: Optional[str] = None
    PORT: Optional[int] = None
    ROUTE: Optional[str] = None

    def URL_create(
            self,
            protocol: Optional[str] = None,
            host: Optional[str] = None,
            port: Optional[int] = None,
            route: Optional[str] = None,
    ) -> str:
        if protocol is None:
            protocol = self.PROTOCOL or "http"
        if host is None:
            host = self.HOST or "localhost"
        if port is None:
            port = self.PORT or 80
        if route is None:
            route = self.ROUTE or ""

        if host == "0.0.0.0":
            host = "localhost"

        while route.startswith("/"):
            route = route[1:]

        url = f"{protocol}://{host}:{port}/{route}"
        return url


# =====================================================================================================================
