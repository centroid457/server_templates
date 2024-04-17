import os
import time

import pytest
import pathlib
import shutil
from tempfile import TemporaryDirectory
from typing import *
from configparser import ConfigParser
import requests

from server_templates import *


# =====================================================================================================================
class Test__Client:
    PORT_TEST: int = 8088

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def setup_method(self, method):
        pass

    # -----------------------------------------------------------------------------------------------------------------
    def test__UrlCreator(self):
        class Victim(UrlCreator):
            PROTOCOL: str = "http"
            HOST: str = "host"
            PORT: int = 80
            ROUTE: str = "route"

        victim = Victim()
        assert victim.URL_create() == "http://host:80/route"
        assert victim.URL_create(host="host2") == "http://host2:80/route"
        assert victim.URL_create(port=8080) == "http://host:8080/route"
        assert victim.URL_create(route="") == "http://host:80/"
        assert victim.URL_create(route="route2") == "http://host:80/route2"

    # -----------------------------------------------------------------------------------------------------------------
    def test__RequestItem(self):
        TEST_DATA = {'test_data_key': 1}

        # SERVER -------------------------------------
        class Server(ServerAiohttpBase):
            PORT = self.PORT_TEST
            test_data = {}

            async def response_post__test_post(self, request) -> web.Response:
                self.test_data = await request.json()
                return web.json_response(data=self.test_data)

            async def response_get_json__test_get_json(self, request) -> web.Response:
                return web.json_response(data=self.test_data)

        server = Server()
        server.start()

        # check MANUALLY ----------------------------
        response = requests.post(url=f"http://localhost:{server.PORT}/test_post", timeout=1, json=TEST_DATA)
        assert response.json() == TEST_DATA

        # check VICTIM ------------------------------
        class Victim(Client_RequestItem):
            START_ON_INIT = True
            PORT = self.PORT_TEST
            ROUTE = "test_post"

        victim = Victim(body=TEST_DATA)
        victim.wait()
        assert victim.RESPONSE.ok
        assert victim.RESPONSE.json() == TEST_DATA

        class Victim(Client_RequestItem):
            START_ON_INIT = True
            PORT = self.PORT_TEST
            ROUTE = "test_get_json"
            METHOD = ResponseMethod.GET

        victim = Victim(body=TEST_DATA)
        victim.wait()
        assert victim.RESPONSE.ok
        assert victim.RESPONSE.json() == TEST_DATA

    # -----------------------------------------------------------------------------------------------------------------
    def test__RequestsStack(self):
        TEST_DATA = {'test_data_key': 1}

        # SERVER -------------------------------------
        class Server(ServerAiohttpBase):
            PORT = self.PORT_TEST + 1
            test_data = {}

            async def response_post__test_post(self, request) -> web.Response:
                self.test_data = await request.json()
                return web.json_response(data=self.test_data)

            async def response_get_json__test_get_json(self, request) -> web.Response:
                return web.json_response(data=self.test_data)

        server = Server()
        server.start()

        # check MANUALLY ----------------------------
        response = requests.post(url=f"http://localhost:{server.PORT}/test_post", timeout=1, json=TEST_DATA)
        assert response.json() == TEST_DATA

        # check VICTIM ------------------------------
        class ClientRequestItem_1(Client_RequestItem):
            PORT = Server.PORT
            ROUTE = "test_post"

        class Victim(Client_RequestsStack):
            REQUEST_CLS = ClientRequestItem_1

        victim = Victim()

        assert server.test_data["test_data_key"] == 1
        victim.send(body={'test_data_key': 2})
        victim.wait()
        assert server.test_data["test_data_key"] == 2


# =====================================================================================================================
