import time
from testplans import TestCaseBase
from . import example_tc1_direct


class TestCase(example_tc1_direct.TestCase):
    DESCRIPTION = "copy1"
