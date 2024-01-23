import pathlib
from typing import *
from aiohttp import web

from .routes import setup_routes


# =====================================================================================================================


# =====================================================================================================================
class ServerAiohttp:
    _app: web.Application

    def __init__(self):
        self._app: web.Application = web.Application()

    def run(self) -> None:
        setup_routes(self._app)
        web.run_app(self._app)


# =====================================================================================================================
