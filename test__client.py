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
            response = requests.post(url=f"http://{host_wrong}/", timeout=0.2, json=TEST_DATA)
            assert False
        except:
            assert True

        # check VICTIM ------------------------------
        class VictimPost(Client_RequestItem):
            HOST = host_wrong
            START_ON_INIT = True
            TIMEOUT_SEND = 0.2

        for _ in range(2):
            victim = VictimPost(body=TEST_DATA)
            victim.wait()
            assert not victim.check_success()

    # -----------------------------------------------------------------------------------------------------------------
    # def test__noserver_timeout(self):
    #     TEST_DATA = {'value': 1}
    #     host_wrong = "host_wrong"
    #
    #     # check MANUALLY ----------------------------
    #     print()
    #     print()
    #     print()
    #     print()
    #     for timeout_item in [0.5, 1.0, 1.5]:
    #         time_start = time.time()
    #         try:
    #             response = requests.post(url=f"http://{host_wrong}/", timeout=timeout_item, json=TEST_DATA)
    #             assert False
    #         except:
    #             assert True
    #
    #         time_finish = time.time()
    #         time_period = time_finish - time_start
    #
    #         print(f"{time_start=}/{time_finish=}/{time_period=}")
    #         assert time_period >= timeout_item
    #         assert time_period < timeout_item * 3
    #
    #     # check VICTIM ------------------------------
    #     # class VictimPost(Client_RequestItem):
    #     #     HOST = host_wrong
    #     #     START_ON_INIT = True
    #     #     TIMEOUT_SEND = 0.5
    #     #
    #     #
    #     # for _ in range(1):
    #     #     victim = VictimPost(body=TEST_DATA)
    #     #     victim.wait()
    #     #     assert not victim.check_success()


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
            response = requests.post(url=f"http://{host_wrong}/", timeout=0.2, json=TEST_DATA)
            assert False
        except:
            assert True

        # check VICTIM ------------------------------
        class ClientRequestItem_1(Client_RequestItem):
            HOST = host_wrong
            TIMEOUT_SEND = 0.2

        class Victim(Client_RequestsStack):
            REQUEST_CLS = ClientRequestItem_1

        victim = Victim()

        for index in range(SEND_COUNT):
            victim.send(body={'index': index})
            assert not victim.check_success()

        victim.wait()
        assert not victim.check_success()
        assert len(victim.stack) == SEND_COUNT


# =====================================================================================================================
