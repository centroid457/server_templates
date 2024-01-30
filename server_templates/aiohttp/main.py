import pathlib
import time
from typing import *
from aiohttp import web
import yaml

import asyncio
# from PyQt5.QtCore import QThread
from threading import Thread


# =====================================================================================================================
pass


# =====================================================================================================================
class ServerAiohttpBase(Thread):
    # SETTINGS -----------------------------
    CONFIG_FILEPATH: Union[pathlib.Path, str] = pathlib.Path(__file__).parent / 'aiohttp_config.yaml'

    # AUX ----------------------------------
    _app: web.Application
    data: Any

    def __init__(self, data: Any = None):
        super().__init__()
        self.CONFIG_FILEPATH: pathlib.Path = pathlib.Path(self.CONFIG_FILEPATH)

        self.data = data
        self._app: web.Application = web.Application()

    @property
    def SETTINGS__ROUTES_GET(self) -> Dict[str, Callable]:
        result = {
            '/': self.response__index,
            '/start': self.response__start,
            '/stop': self.response__stop,
        }
        return result

    # =================================================================================================================
    def run(self) -> None:
        self.setup_routes()
        self.apply_config()

        web.run_app(app=self._app)
        # thread = threading.Thread(target=web.run_app, kwargs={"app": self._app, })
        # print(f"{self.__class__.__name__} started in thread")
        # thread.start()
        # thread.join()

    # =================================================================================================================
    def apply_config(self, config_filepath=None):
        config_filepath = config_filepath or self.CONFIG_FILEPATH
        if config_filepath and config_filepath.exists():
            with open(config_filepath) as f:
                config = yaml.safe_load(f)
                self._app["config"] = config
            print(f"{self._app['config']=}")
        else:
            msg = f"[WARN] no file {self.CONFIG_FILEPATH=}"
            print(msg)
            self._app["config"] = {}

        # self._app['config']={'postgres': {'user': 'aiohttpdemo_user', 'password': 'aiohttpdemo_pass', 'host': 'localhost', 'port': 5432}}

    def setup_routes(self):
        for route, response in self.SETTINGS__ROUTES_GET.items():
            self._app.router.add_get(route, response)

    # =================================================================================================================
    async def response__index(self, request):
        msg = """
    <!doctype html>
    <html lang="en-US">
      <head>
        <meta charset="utf-8" />
        <title>INDEX</title>
        <meta http-equiv="refresh" content="2; url=/" />
      </head>
      <body>
        response__index<br />
        PROGRESS = %(progress)s<br />
        <a href="/start">START</a><br />
        <a href="/stop">STOP</a><br />
      </body>
    </html>
        """
        if self.data and self.data.progress is not None:
            msg = msg%{"progress": self.data.progress}
        # print(msg)
        print(11)
        # await asyncio.sleep(3)
        print(2222)
        return web.Response(text=msg, content_type='text/html')

    async def response__start(self, request):
        msg = """
    <!doctype html>
    <html lang="en-US">
      <head>
        <meta charset="utf-8" />
        <title>INDEX</title>
        <meta http-equiv="refresh" content="1; url=/" />
      </head>
      <body>
        response__start<br />
        <p><a href="/">Redirect</a></p>
      </body>
    </html>
        """
        # print(msg)
        self.data.signal__tp_start.emit()
        return web.Response(text=msg, content_type='text/html')

    async def response__stop(self, request):
        msg = """
        <!doctype html>
        <html lang="en-US">
          <head>
            <meta charset="utf-8" />
            <title>INDEX</title>
            <meta http-equiv="refresh" content="1; url=/" />
          </head>
          <body>
            response__stop<br />
            <p><a href="/">Redirect</a></p>
          </body>
        </html>
        """
        # print(msg)
        self.data.signal__tp_stop.emit()
        return web.Response(text=msg, content_type='text/html')


# =====================================================================================================================
