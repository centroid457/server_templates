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
# FIXME: CANT SEPARATE TESTS!!!! WORK ONLY BY

class Test__ServerAiohttp:
    PORT_TEST1: int = 8081

    victim_1 = None
    victim_2 = None

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
        TEST_DATA = {'test_data_key_1': 1}

        class ServerAiohttp_1(ServerAiohttpBase):
            PORT = self.PORT_TEST1
            test_data = None

            async def response_post__test1(self, request) -> web.Response:
                self.test_data = await request.json()
                return web.json_response(data=TEST_DATA)

            async def response_get_json__test1(self, request) -> web.Response:
                return web.json_response(data=TEST_DATA)

        self.Victim_1 = ServerAiohttp_1
        self.victim_1 = self.Victim_1()

        class ServerAiohttp_2(ServerAiohttpBase):
            PORT = self.PORT_TEST1 + 1

        self.Victim_2 = ServerAiohttp_2
        self.victim_2 = self.Victim_2()

        # WORK ==============================================
        self.victim_1.start()
        response = requests.get(url=f"http://localhost:{self.victim_1.PORT}/", timeout=1)

        # double start DEPandant -------------------------
        try:
            self.victim_1.run()
            assert False
        except:
            pass

        # double start INDEPandant ------------------------
        self.victim_2.start()
        response = requests.get(url=f"http://localhost:{self.victim_2.PORT}/", timeout=1)

        # test__GET_INDEX ----------------------------------
        response = requests.get(url=f"http://localhost:{self.victim_1.PORT}/api_index", timeout=1)
        assert f'/api_index' in self.victim_1._ROUTES["get_html"]
        assert f'/api_index' in response.text

        # test__GET_JSON ----------------------------------
        response = requests.get(url=f"http://localhost:{self.victim_1.PORT}/test1", timeout=1)
        assert f'/test1' in self.victim_1._ROUTES["get_json"]
        assert f'/{self.victim_1._ROUTE_NAME_PREFIX_HTML_FOR_JSON}test1' in self.victim_1._ROUTES["get_html"]
        assert response.json() == TEST_DATA

        response = requests.get(url=f"http://localhost:{self.victim_1.PORT}/{self.victim_1._ROUTE_NAME_PREFIX_HTML_FOR_JSON}test1", timeout=1)
        assert 'test_data_key_1' in response.text

        # test__POST ----------------------------------
        response = requests.post(url=f"http://localhost:{self.victim_1.PORT}/test1", timeout=1, json=TEST_DATA)
        assert f'/test1' in self.victim_1._ROUTES["post"]
        assert self.victim_1.test_data == TEST_DATA
        assert response.json() == TEST_DATA


# =====================================================================================================================
