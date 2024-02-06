import pathlib
import time
import json
from typing import *
import functools

import asyncio
from aiohttp import web
import yaml

from PyQt5.QtCore import QThread
# from threading import Thread

from object_info import ObjectInfo


# =====================================================================================================================
Type__Self = Any
Type__Request = Any


def decorator__log_request_response(func: Callable[[Type__Self, Type__Request], Coroutine[Any, Any, web.Response]]):
    @functools.wraps(func)
    async def _wrapper(self, request):
        # ObjectInfo(request).print()

        response = await func(self, request)
        # ObjectInfo(response).print()

        print(f"API access[from={request.remote=}/to={request.host=}][{self.__class__.__name__}.{func.__name__}()][{response.status=}]")
        """
        API access[request.remote=172.24.128.1/request.host='starichenko']          #MYSELF
        API access[request.remote=192.168.75.1/request.host='192.168.75.144:80']    #from CoWorker
        """
        return response
    return _wrapper


# =====================================================================================================================
class ServerAiohttpBase(QThread):
    # SETTINGS -----------------------------
    CONFIG_FILEPATH: Union[pathlib.Path, str] = pathlib.Path(__file__).parent / 'aiohttp_config.yaml'
    PORT: Optional[int] = 80  # None==8080/directWeb==80

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

        web.run_app(app=self._app, port=self.PORT)
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
            request: Any = None,
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
        body_header = f"<a href='/'>HOME</a>/{name}<br />"
        if request:
            body_header += f"request from={request.remote=}/to={request.host=}<br />"

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
                <p>{body_header}</p>
                <p>{data}</p>
            </body>
        </html>
        """
        return result

    def html_block__api_index(self) -> str:
        html_block = f""
        for group, names in self._route_groups.items():
            html_block += f"{group.upper()}:<br />"
            for name in names:
                if group == "get":
                    html_block += f"<a href='{name}'>{name}</a><br />"
                else:
                    html_block += f"{name}<br />"

            html_block += f"<br />"
        return html_block

    # =================================================================================================================
    async def response_get__(self, request) -> web.Response:
        return await self.response_get__api_index(request)

    async def response_get__api_index(self, request) -> web.Response:
        # HTML --------------------------------------------------
        page_name = "API_INDEX"
        html = self.html_create(name=page_name, data=self.html_block__api_index(), request=request)
        return web.Response(text=html, content_type='text/html')


# =====================================================================================================================
class ServerAiohttp_Example(ServerAiohttpBase):
    # @decorator__log_request_response
    async def response_get__(self, request) -> web.Response:
        # --------------------------
        progress = 0
        if self.data and self.data.progress is not None:
            progress = self.data.progress
        # --------------------------
        html_block = f"[PROGRESS = {progress}%]<br /><br />" + self.html_block__api_index()

        # HTML --------------------------------------------------
        page_name = "API_INDEX"
        html = self.html_create(name=page_name, data=html_block, redirect_time=2, request=request)
        return web.Response(text=html, content_type='text/html')

    @decorator__log_request_response
    async def response_get__start(self, request) -> web.Response:
        self.data.signal__tp_start.emit()

        # HTML --------------------------------------------------
        page_name = "START"
        html = self.html_create(name=page_name, redirect_time=1, request=request)
        return web.Response(text=html, content_type='text/html')

    @decorator__log_request_response
    async def response_get__stop(self, request) -> web.Response:
        self.data.signal__tp_stop.emit()

        # HTML --------------------------------------------------
        page_name = "STOP"
        html = self.html_create(name=page_name, redirect_time=1, request=request)
        return web.Response(text=html, content_type='text/html')

    @decorator__log_request_response
    async def response_post__start(self, request) -> web.Response:
        # return self.response_get__start(request)  # this is will not work!
        response = web.json_response(data={})
        return response

    @decorator__log_request_response
    async def response_post__stop(self, request) -> web.Response:
        response = web.json_response(data={})
        return response

    @decorator__log_request_response
    async def response_get__info_json(self, request) -> web.Response:
        body: dict = self.data.info_get()
        response = web.json_response(data=body)
        return response

    @decorator__log_request_response
    async def response_get__info_html(self, request) -> web.Response:
        """
        this is only for pretty view
        """
        # HTML --------------------------------------------------
        page_name = "INFO_HTML"
        html = self.html_create(name=page_name, data=self.data.info_get(), request=request)
        return web.Response(text=html, content_type='text/html')


# =====================================================================================================================
