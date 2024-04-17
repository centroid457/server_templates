import os
import time

from object_info import ObjectInfo

import pytest
import pathlib
import shutil
from tempfile import TemporaryDirectory
from typing import *
from configparser import ConfigParser
import requests

from server_templates import *


# =====================================================================================================================
class Test__Server_FastApi:
    @classmethod
    def setup_class(cls):
        pass

        # server = ServerFastApi(create_app__FastApi())
        # server.start()

    @classmethod
    def teardown_class(cls):
        pass

    def setup_method(self, method):
        pass

    # -----------------------------------------------------------------------------------------------------------------
    def test__types(self):
        # WORK ==============================================
        response = requests.get(url=f"http://localhost:8000/types/int", timeout=1)
        # ObjectInfo(response).print()

        response = requests.get(url=f"http://localhost:8000/types/str", timeout=1)
        # ObjectInfo(response).print()

        response = requests.get(url=f"http://localhost:8000/types/dict", timeout=1)
        ObjectInfo(response).print()

    def test__post(self):
        # PREPARE ==============================================
        TEST_DATA = {'test_data_key': 1}

        # WORK ==============================================
        response = requests.post(url=f"http://localhost:8000/post/start", timeout=1, json=TEST_DATA)
        ObjectInfo(response).print()

        # assert response.json() == TEST_DATA


# =====================================================================================================================
