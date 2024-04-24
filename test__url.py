import os
import time

import pytest
import pathlib
import shutil
from tempfile import TemporaryDirectory
from typing import *
from configparser import ConfigParser
import requests

from server_templates.url import UrlCreator


# =====================================================================================================================
class Test__Url:
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
        assert victim.URL_create(route="/route2") == "http://host:80/route2"
        assert victim.URL_create(route="//route2") == "http://host:80/route2"
        assert victim.URL_create(route="//////route2") == "http://host:80/route2"
        assert victim.URL_create(route="/route2/") == "http://host:80/route2/"
        assert victim.URL_create(route="/route2////") == "http://host:80/route2////"
        assert victim.URL_create(route="/route2/route3") == "http://host:80/route2/route3"


# =====================================================================================================================
