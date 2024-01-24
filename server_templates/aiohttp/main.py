import pathlib
from typing import *
from aiohttp import web
import yaml
from threading import Thread


# =====================================================================================================================
BASE_DIR = pathlib.Path(__file__).parent


# =====================================================================================================================
class ServerAiohttpBase(Thread):
    # SETTINGS =============================
    CONFIG_PATH = BASE_DIR / 'config.yaml'

    # AUX ==================================
    _app: web.Application
    data: Any

    def __init__(self, data: Any = None):
        super().__init__()

        self.ROUTES_GET: Dict[str, Callable] = {
            '/': self.response__index,
            '/start': self.response__start,
            '/stop': self.response__stop,
        }

        self.data = data
        self._app: web.Application = web.Application()

    def run(self) -> None:
        self.setup_routes()
        self.apply_config()
        web.run_app(self._app)

    def apply_config(self, path=None):
        path = path or self.CONFIG_PATH
        if path:
            with open(path) as f:
                config = yaml.safe_load(f)
                self._app["config"] = config
        print(f"{self._app['config']=}")
        # self._app['config']={'postgres': {'user': 'aiohttpdemo_user', 'password': 'aiohttpdemo_pass', 'host': 'localhost', 'port': 5432}}

    def setup_routes(self):
        for route, response in self.ROUTES_GET.items():
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
        print(msg)
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
        print(msg)
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
        print(msg)
        self.data.signal__tp_stop.emit()
        return web.Response(text=msg, content_type='text/html')


# =====================================================================================================================
