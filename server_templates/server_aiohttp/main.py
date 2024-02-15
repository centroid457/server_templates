import pathlib
import time
import json
from typing import *
import functools

import asyncio

import requests
from aiohttp import web
import aiohttp
import yaml

from PyQt5.QtCore import QThread

from object_info import ObjectInfo


# =====================================================================================================================
Type__Self = Any
Type__Request = Any


class Exx__AiohttpSeverStartSameAddress(Exception):
    pass


def decorator__log_request_response(func: Callable[[Type__Self, Type__Request], Coroutine[Any, Any, web.Response]]):
    @functools.wraps(func)
    async def _wrapper(self, request):
        # ObjectInfo(request).print()

        response = await func(self, request)
        # ObjectInfo(response).print()
        # print(f"API access[from={request.remote=}/to={request.host=}][{self.__class__.__name__}.{func.__name__}()][{response.status=}]")
        return response

    return _wrapper


# =====================================================================================================================
class ServerAiohttpBase(QThread):
    """
    NOTE: some problems withing PYTEST only! you can do any instances in one program!

    SEE testplans.TpApi as example
    """
    # SETTINGS -----------------------------
    START_ON_INIT: bool = False
    CONFIG_FILEPATH: Union[pathlib.Path, str] = pathlib.Path(__file__).parent / 'aiohttp_config.yaml'
    PORT: Optional[int] = 80  # None==8080/directWeb==80

    # AUX ----------------------------------
    _ROUTE_FUNC_START_PATTERN: str = "response_%s__"
    _ROUTE_NAME_PREFIX_HTML_FOR_JSON: str = "html__"
    _app: web.Application
    _ROUTES: Dict[str, List[str]] = {
        "get_html": [],
        "get_json": [],
        "post": [],
    }
    data: Any

    def __init__(self, data: Any = None):
        """
        :param data: just to keep as further standard
        """
        super().__init__()
        self.CONFIG_FILEPATH: pathlib.Path = pathlib.Path(self.CONFIG_FILEPATH)
        self.data = data

    # =================================================================================================================
    def run(self) -> None:
        """
        NOTE: this will block process!
        but if start() in thread - it would be OK!

        EXCEPTION will not catch from start!!! but will CAUSE SYS_EXIT!!!
        """
        try:
            self._app: web.Application = web.Application()
            self.setup_routes()
            self.apply_config()
            web.run_app(app=self._app, port=self.PORT)
            # this will not catch!!! cause of thread maybe!!!
        except Exception as exx:
            msg = f"[ERROR]started same server address {exx!r}"
            print(msg)
            raise Exx__AiohttpSeverStartSameAddress(msg)  # DON'T DELETE RAISE! - IT IS VERY NECESSARY/IMPORTANT for tests!

    def start(self, *args):
        if not self.isRunning():
            super().start()

    def __server_stop_start(self):
        """
        just as info
        """
        self._app.shutdown()
        self._app.startup()

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
            for group_name, group_list in self._ROUTES.items():
                group_name_start = self._ROUTE_FUNC_START_PATTERN % group_name
                if not attr_name.startswith(group_name_start):
                    continue

                route_name_wo_slash = f'{attr_name.replace(group_name_start, "")}'
                route_name_w_slash = f'/{route_name_wo_slash}'
                self._ROUTES[group_name].append(route_name_w_slash)
                if group_name == 'get_html':
                    self._app.router.add_get(route_name_w_slash, getattr(self, attr_name))
                elif group_name == 'get_json':
                    self._app.router.add_get(route_name_w_slash, getattr(self, attr_name))
                    self._app.router.add_get(f"/{self._ROUTE_NAME_PREFIX_HTML_FOR_JSON}{route_name_wo_slash}", self._response_get_json__converted_to_html)

                    self._ROUTES["get_html"].append(f"/{self._ROUTE_NAME_PREFIX_HTML_FOR_JSON}{route_name_wo_slash}")

                elif group_name == 'post':
                    self._app.router.add_post(route_name_w_slash, getattr(self, attr_name))
                    self._app.router.add_get(route_name_w_slash, self._response_post__converted_to_get)

    # =================================================================================================================
    def html_create(
            self,
            data: Union[None, str, Dict] = None,
            redirect_time: Optional[int] = None,
            redirect_source: Optional[str] = None,
            request: Any = None,
    ) -> str:
        route = request.path
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
        body_header = f"<a href='/'>HOME</a>{route}<br />"
        if request:
            body_header += f"request from={request.remote=}/to={request.host=}<br />"

        # -------------------------------------
        result = f"""
        <!doctype html>
        <html lang="en-US">
            <head>
                <meta charset="utf-8" />
                <title>{route}</title>
                {part_refresh}
            </head>
            <body>
                <p>{body_header}</p>
                <p>{data}</p>
            </body>
        </html>
        """
        return result

    def html_block__api_index(self) -> str:
        html_block = f""
        for group, names in self._ROUTES.items():
            html_block += f"{group.upper()}:<br />"
            for name in names:
                html_block += f"<a href='{name}'>{name}</a><br />"

            html_block += f"<br />"
        return html_block

    # =================================================================================================================
    async def _response_post__converted_to_get(self, request) -> web.Response:
        route = request.path[1:]
        await getattr(self, self._ROUTE_FUNC_START_PATTERN % "post" + route)(request)

        # RESPONSE --------------------------------------------------
        html = self.html_create(data="", request=request, redirect_time=1)
        return web.Response(text=html, content_type='text/html')

    async def _response_get_json__converted_to_html(self, request) -> web.Response:
        route_json = request.path[1:].replace(self._ROUTE_NAME_PREFIX_HTML_FOR_JSON, "")
        response: requests.Response = await getattr(self, self._ROUTE_FUNC_START_PATTERN % "get_json" + route_json)(request)
        data_text = response.text   # no json/data here in instance!
        data_json = json.loads(data_text)

        # RESPONSE --------------------------------------------------
        html = self.html_create(data=data_json, request=request)
        return web.Response(text=html, content_type='text/html')

    # =================================================================================================================
    async def response_get_html__(self, request) -> web.Response:
        return await self.response_get_html__api_index(request)

    async def response_get_html__api_index(self, request) -> web.Response:
        # RESPONSE --------------------------------------------------
        html = self.html_create(data=self.html_block__api_index(), request=request)
        return web.Response(text=html, content_type='text/html')

    # THIS IS AS HELP COMMENT!
    # @decorator__log_request_response
    # async def response_post__start(self, request) -> web.Response:
    #     # return self.response_get__start(request)  # this is will not work!
    #     self.data.signal__tp_start.emit()
    #     test_data = await request.json()  # dont use

    #     # RESPONSE --------------------------------------------------
    #     response = web.json_response(data={})
    #     return response


# =====================================================================================================================
