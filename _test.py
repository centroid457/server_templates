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
class Test__ServerAiohttp:
    # FIXME: CANT SEPARATE TESTS!!!! WORK ONLY one BY one
    PORT_TEST: int = 8081

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def setup_method(self, method):
        pass

    # -----------------------------------------------------------------------------------------------------------------
    def test__ALL(self):
        # PREPARE ==============================================
        TEST_DATA = {'test_data_key': 1}

        class Victim(ServerAiohttpBase):
            PORT = self.PORT_TEST
            test_data = {}

            async def response_post__test_post(self, request) -> web.Response:
                self.test_data = await request.json()
                return web.json_response(data=self.test_data)

            async def response_get_json__test_get_json(self, request) -> web.Response:
                return web.json_response(data=self.test_data)

        self.victim = Victim()

        class Victim2(ServerAiohttpBase):
            PORT = self.PORT_TEST + 1

        self.victim_2 = Victim2()

        # WORK ==============================================
        self.victim.start()
        response = requests.get(url=f"http://localhost:{self.victim.PORT}/", timeout=1)

        # double start DEPandant -------------------------
        try:
            self.victim.run()
            assert False
        except:
            pass

        # double start INDEPandant ------------------------
        self.victim_2.start()
        response = requests.get(url=f"http://localhost:{self.victim_2.PORT}/", timeout=1)

        # test__GET_INDEX ----------------------------------
        response = requests.get(url=f"http://localhost:{self.victim.PORT}/api_index", timeout=1)
        assert f'/api_index' in self.victim._ROUTES["get_html"]
        assert f'/api_index' in response.text

        # test__POST ----------------------------------
        response = requests.get(url=f"http://localhost:{self.victim.PORT}/test_get_json", timeout=1)
        assert response.json() == {}

        response = requests.post(url=f"http://localhost:{self.victim.PORT}/test_post", timeout=1, json=TEST_DATA)
        assert f'/test_post' in self.victim._ROUTES["post"]
        assert self.victim.test_data == TEST_DATA
        assert response.json() == TEST_DATA

        # test__GET_JSON ----------------------------------
        response = requests.get(url=f"http://localhost:{self.victim.PORT}/test_get_json", timeout=1)
        assert f'/test_get_json' in self.victim._ROUTES["get_json"]
        assert f'/{self.victim._ROUTE_NAME_PREFIX_HTML_FOR_JSON}test_get_json' in self.victim._ROUTES["get_html"]
        assert response.json() == TEST_DATA

        response = requests.get(url=f"http://localhost:{self.victim.PORT}/{self.victim._ROUTE_NAME_PREFIX_HTML_FOR_JSON}test_get_json", timeout=1)
        assert 'test_data_key' in response.text

        # test__404 ----------------------------------
        response = requests.get(url=f"http://localhost:{self.victim.PORT}/test404", timeout=1)
        assert not response.ok
        assert response.status_code == 404

        # test__STOP/START ----------------------------------
        response = requests.get(url=f"http://localhost:{self.victim.PORT}/", timeout=0.3)
        assert response.ok
        assert response.status_code == 200

        self.victim._app.shutdown()
        try:
            response = requests.get(url=f"http://localhost:{self.victim.PORT}/", timeout=0.3)
            assert False
        except:
            assert True

        self.victim._app.startup()
        response = requests.get(url=f"http://localhost:{self.victim.PORT}/", timeout=0.3)
        assert response.ok
        assert response.status_code == 200


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

    def test__RequestItem(self):
        # PREPARE ==============================================
        TEST_DATA = {'test_data_key': 1}

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

        response = requests.post(url=f"http://localhost:{server.PORT}/test_post", timeout=1, json=TEST_DATA)
        assert response.json() == TEST_DATA

        class Victim(RequestItem):
            PORT: int = self.PORT_TEST
            ROUTE: str = "test_post"

        victim = Victim(body=TEST_DATA)
        victim.start()
        victim.wait()
        assert victim.RESPONSE.ok
        assert victim.RESPONSE.json() == TEST_DATA


# =====================================================================================================================
