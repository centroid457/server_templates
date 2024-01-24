import pathlib
from typing import *
from aiohttp import web

from .routes import setup_routes
from .settings import config


# =====================================================================================================================


# =====================================================================================================================
class ServerAiohttp:
    _app: web.Application

    def __init__(self):
        self._app: web.Application = web.Application()

    def run(self) -> None:
        setup_routes(self._app)
        self._app["config"] = config
        print(f"{self._app['config']=}")
        # self._app['config']={'postgres': {'user': 'aiohttpdemo_user', 'password': 'aiohttpdemo_pass', 'host': 'localhost', 'port': 5432}}
        web.run_app(self._app)


# =====================================================================================================================
