import server_templates
import pathlib
from testplans import TpMultyDutBase

class Tp(TpMultyDutBase):
    START_GUI = True

tp = Tp()
# print(tp.DIRPATH_TCS)
# print(tp.DIRPATH_TCS.exists())
# print(pathlib.Path.cwd())
thread = server_templates.ServerAiohttpBase(tp).run()


# # ====================================
# from setuptools import find_packages
#
# pkgs = find_packages("server_templates")
#
# print(pkgs)
# for name in pkgs:
#     print(f"\t{name}")
