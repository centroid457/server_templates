import pathlib
import time
import json
from typing import *

import asyncio
from aiohttp import web
import yaml

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
    _ROUTE_FUNC_START_PATTERN: str = "response_%s__"
    _app: web.Application
    _route_groups: Dict[str, List[str]] = {
        "get": [],
        "post": [],
    }
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

    # =================================================================================================================
    def setup_routes(self):
        for attr_name in dir(self):
            for group_name, group_list in self._route_groups.items():
                group_name_start = self._ROUTE_FUNC_START_PATTERN % group_name
                if not attr_name.startswith(group_name_start):
                    continue

                route_name = f'/{attr_name.replace(group_name_start, "")}'
                self._route_groups[group_name].append(route_name)
                if group_name == 'get':
                    self._app.router.add_get(route_name, getattr(self, attr_name))
                elif group_name == 'post':
                    self._app.router.add_post(route_name, getattr(self, attr_name))

        # print(f'{self._route_groups=}')

    # =================================================================================================================
    def html_create(
            self,
            name: str,
            data: Union[None, str, Dict] = None,
            redirect_time: Optional[int] = None,
            redirect_source: Optional[str] = None,
    ) -> str:
        data = data or ""

        # -------------------------------------
        part_refresh = ""
        if redirect_time:
            part_refresh = f"<meta http-equiv='refresh' content='{redirect_time}; url=/' />"

        # -------------------------------------
        if isinstance(data, str):
            pass

        elif isinstance(data, dict):
            data = json.dumps(data, indent=4)
            # body_html = body_pretty.replace("\n", "<br />\n")     # dont need!
            data = f"<pre>{data}</pre>"

        else:
            data = str(data)

        # -------------------------------------
        result = f"""
        <!doctype html>
        <html lang="en-US">
            <head>
                <meta charset="utf-8" />
                <title>{name}</title>
                {part_refresh}
            </head>
            <body>
                <p><a href="/">HOME</a>/{name}</p>
                <p>{data}</p>
            </body>
        </html>
        """
        return result

    # =================================================================================================================
    async def response_get__(self, request) -> web.Response:
        # --------------------------
        progress = 0
        if self.data and self.data.progress is not None:
            progress = self.data.progress
        # --------------------------
        html_block = f"[PROGRESS = {progress}%]<br /><br />"
        for group, names in self._route_groups.items():
            html_block += f"{group.upper()}:<br />"
            for name in names:
                html_block += f"<a href='{name}'>{name}</a><br />"

            html_block += f"<br />"

        # HTML --------------------------------------------------
        page_name = "*INDEX"
        html = self.html_create(name=page_name, data=html_block, redirect_time=2)
        return web.Response(text=html, content_type='text/html')

    async def response_get__start(self, request) -> web.Response:
        self.data.signal__tp_start.emit()

        # HTML --------------------------------------------------
        page_name = "START"
        html = self.html_create(name=page_name, redirect_time=1)
        return web.Response(text=html, content_type='text/html')

    async def response_get__stop(self, request) -> web.Response:
        self.data.signal__tp_stop.emit()

        # HTML --------------------------------------------------
        page_name = "STOP"
        html = self.html_create(name=page_name, redirect_time=1)
        return web.Response(text=html, content_type='text/html')

    async def response_post__start(self, request) -> web.Response:
        return self.response_get__start(request)

    async def response_post__stop(self, request) -> web.Response:
        return self.response_get__stop(request)

    async def response_get__info_json(self, request) -> web.Response:
        body: dict = self.data.info_get()
        response = web.json_response(body)
        return response

    async def response_get__info_html(self, request) -> web.Response:
        """
        this is only for pretty view
        """
        # HTML --------------------------------------------------
        page_name = "INFO_HTML"
        html = self.html_create(name=page_name, data=self.data.info_get())
        return web.Response(text=html, content_type='text/html')


# =====================================================================================================================
