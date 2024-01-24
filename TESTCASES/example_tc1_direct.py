import time
from testplans import TestCaseBase


class TestCase(TestCaseBase):
    ACYNC = False
    DESCRIPTION = "direct1"
    SETTINGS = {}   # DONT DELETE!

    def run_wrapped(self) -> bool:
        time.sleep(0.2)
        self.details_update({"detail_value": self.DUT.VALUE})
        return self.DUT.VALUE
