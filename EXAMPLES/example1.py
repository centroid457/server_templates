import server_templates
import pathlib
from testplans import TpMultyDutBase
import time


class Tp(TpMultyDutBase):
    START_GUI = False


tp = Tp()
# print(tp.DIRPATH_TCS)
# print(tp.DIRPATH_TCS.exists())
# print(pathlib.Path.cwd())
server = server_templates.ServerAiohttpBase(tp)
server.start()
server.join()
