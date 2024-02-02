import pathlib
import time
import json
from typing import *
from aiohttp import web
import yaml

import asyncio
# from PyQt5.QtCore import QThread
from threading import Thread
from object_info import ObjectInfo


# =====================================================================================================================
pass


# =====================================================================================================================
class ServerAiohttpBase(Thread):
    # SETTINGS -----------------------------
    CONFIG_FILEPATH: Union[pathlib.Path, str] = pathlib.Path(__file__).parent / 'aiohttp_config.yaml'

    # AUX ----------------------------------
    _app: web.Application
    _routes_applied: List[str] = []
    data: Any

    def __init__(self, data: Any = None):
        super().__init__()
        self.CONFIG_FILEPATH: pathlib.Path = pathlib.Path(self.CONFIG_FILEPATH)

        self.data = data
        self._app: web.Application = web.Application()

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
        """
        RULES:
        1. USE ONLY GET!!! no need POST/PUT/!
        """
        self._routes_applied = []
        response__startswith = "response__"
        for attr_name in dir(self):
            if not attr_name.startswith(response__startswith):
                continue
            route = f'/{attr_name.replace(response__startswith, "")}'
            self._routes_applied.append(route)
            self._app.router.add_get(route, getattr(self, attr_name))

        # # ---------------------------------------------------------
        # ROUTES_GET = {
        #     '/': self.response__,
        #     '/start': self.response__start,
        #     '/stop': self.response__stop,
        #     '/info': self.response__info,
        # }
        # for route, response in ROUTES_GET.items():
        #     self._app.router.add_get(route, response)
        #
        # # ---------------------------------------------------------
        # ROUTES_POST = {
        #     '/start': self.response__start,
        #     '/stop': self.response__stop,
        # }
        # for route, response in ROUTES_POST.items():
        #     self._app.router.add_post(route, response)

    # =================================================================================================================
    def html_pretty_from_any(self, body: Union[str, Dict]) -> str:
        body_pretty = str(body)
        if isinstance(body, dict):
            body_pretty = json.dumps(body, indent=4)
            # body_html = body_pretty.replace("\n", "<br />\n")     # dont need!

        body_html__space_save = f"<pre>{body_pretty}</pre>"
        return body_html__space_save

    # =================================================================================================================
    async def response__(self, request):
        # --------------------------
        progress = 0
        if self.data and self.data.progress is not None:
            progress = self.data.progress
        # --------------------------
        routes_links = ""
        for route in self._routes_applied:
            routes_links += f"<a href='{route}'>{route}</a><br />\n"

        # result -------------------
        name = "INDEX"
        msg = f"""
        <!doctype html>
        <html lang="en-US">
            <head>
                <meta charset="utf-8" />
                <title>{name}</title>
                <meta http-equiv="refresh" content="2; url=/" />
            </head>
            <body>
                {name}<br />
                PROGRESS = {progress}%<br />
                {routes_links}
            </body>
        </html>
        """
        return web.Response(text=msg, content_type='text/html')

    async def response__start(self, request):
        name = "START"
        msg = f"""
        <!doctype html>
        <html lang="en-US">
            <head>
                <meta charset="utf-8" />
                <title>{name}</title>
                <meta http-equiv="refresh" content="1; url=/" />
            </head>
            <body>
                <p>{name}<a href="/">HOME</a></p>
            </body>
        </html>
        """
        # print(msg)
        self.data.signal__tp_start.emit()
        return web.Response(text=msg, content_type='text/html')

    async def response__stop(self, request):
        name = "STOP"
        msg = f"""
        <!doctype html>
        <html lang="en-US">
            <head>
                <meta charset="utf-8" />
                <title>{name}</title>
                <meta http-equiv="refresh" content="1; url=/" />
            </head>
            <body>
                <p>{name}<a href="/">HOME</a></p>
            </body>
        </html>
        """
        self.data.signal__tp_stop.emit()
        return web.Response(text=msg, content_type='text/html')

    async def response__info_json(self, request):
        body: dict = self.data.info_get()
        response = web.json_response(body)
        return response

    async def response__info_html(self, request):
        """
        this is only for pretty view
        """
        body: dict = self.data.info_get()
        body_html = self.html_pretty_from_any(body)

        name = "INFO_HTML"
        msg = f"""
        <!doctype html>
        <html lang="en-US">
            <head>
                <meta charset="utf-8" />
                <title>{name}</title>
            </head>
            <body>
                <p>{name}<a href="/">HOME</a></p>
                <p>{body_html}</p>
            </body>
        </html>
        """
        # for key, value in body.items():
        #     print(f"{key}: {value}")
        return web.Response(text=msg, content_type='text/html')


# =====================================================================================================================
