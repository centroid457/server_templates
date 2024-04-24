import os
import time

import pytest
import pathlib
import shutil
from tempfile import TemporaryDirectory
from typing import *
from configparser import ConfigParser
import requests

from server_templates.client_requests import Client_RequestItem, ResponseMethod, Client_RequestsStack
from server_templates.url import UrlCreator
from server_templates.server_aiohttp import ServerAiohttpBase, web
from server_templates.server_fastapi import ServerFastApi_Thread


# =====================================================================================================================
class Test__RequestItem:
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
    def test__1(self):
        TEST_DATA = {'value': 1}

        # SERVER -------------------------------------
        class Server(ServerFastApi_Thread):
            PORT = self.PORT_TEST

        server = Server()
        server.start()

        assert server.data.dict.get("value") is None

        # check MANUALLY ----------------------------
        response = requests.post(url=f"http://localhost:{server.PORT}/post/dict", timeout=1, json=TEST_DATA)
        assert response.json() == TEST_DATA

        # check VICTIM ------------------------------
        class VictimPost(Client_RequestItem):
            START_ON_INIT = True
            PORT = self.PORT_TEST
            ROUTE = "/post/dict"

        victim = VictimPost(body=TEST_DATA)
        victim.wait()
        assert victim.RESPONSE.ok
        assert victim.RESPONSE.json() == TEST_DATA

        class VictimGet(Client_RequestItem):
            START_ON_INIT = True
            PORT = self.PORT_TEST
            ROUTE = "/return_types/str"
            METHOD = ResponseMethod.GET

        victim = VictimGet(body=TEST_DATA)
        victim.wait()
        assert victim.RESPONSE.ok
        assert victim.RESPONSE.json() == "str"

    # -----------------------------------------------------------------------------------------------------------------
    def test__2_noserver(self):
        TEST_DATA = {'value': 1}
        host_wrong = "host_wrong"

        # check MANUALLY ----------------------------
        try:
            response = requests.post(url=f"http://{host_wrong}/", timeout=1, json=TEST_DATA)
            assert False
        except:
            assert True

        # check VICTIM ------------------------------
        class VictimPost(Client_RequestItem):
            HOST = host_wrong
            START_ON_INIT = True
            TIMEOUT_SEND = 0.3

        for _ in range(10):
            victim = VictimPost(body=TEST_DATA)
            victim.wait()
            assert not victim.check_success()


# =====================================================================================================================
class Test__RequestsStack:
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
    def test__1(self):
        TEST_DATA = {'value': 1}

        # SERVER -------------------------------------
        class Server(ServerFastApi_Thread):
            PORT = self.PORT_TEST + 1

        server = Server()
        server.start()

        # assert server.data.dict.get("value") is None

        # check MANUALLY ----------------------------
        response = requests.post(url=f"http://localhost:{server.PORT}/post/dict", timeout=1, json=TEST_DATA)
        assert response.json() == TEST_DATA

        # check VICTIM ------------------------------
        class ClientRequestItem_1(Client_RequestItem):
            PORT = Server.PORT
            ROUTE = "/post/dict"

        class Victim(Client_RequestsStack):
            REQUEST_CLS = ClientRequestItem_1

        victim = Victim()

        assert server.data.dict.get("value") == 1
        victim.send(body={'value': 2})
        victim.wait()
        assert server.data.dict.get("value") == 2

    # -----------------------------------------------------------------------------------------------------------------
    def test__2_noserver(self):
        SEND_COUNT = 100
        TEST_DATA = {'value': 1}
        host_wrong = "host_wrong"

        # check MANUALLY ----------------------------
        try:
            response = requests.post(url=f"http://{host_wrong}/", timeout=1, json=TEST_DATA)
            assert False
        except:
            assert True

        # check VICTIM ------------------------------
        class ClientRequestItem_1(Client_RequestItem):
            HOST = host_wrong
            TIMEOUT_SEND = 0.3

        class Victim(Client_RequestsStack):
            REQUEST_CLS = ClientRequestItem_1

        victim = Victim()

        for _ in range(SEND_COUNT):
            victim.send(body={'value': 111})
            assert not victim.check_success()

        victim.wait()
        assert not victim.check_success()
        assert len(victim.stack) == SEND_COUNT


# =====================================================================================================================
