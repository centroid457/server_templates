import server_templates
import testplans
thread = server_templates.ServerAiohttpBase(testplans.TpMultyDutBase()).run()


# # ====================================
# from setuptools import find_packages
#
# pkgs = find_packages("server_templates")
#
# print(pkgs)
# for name in pkgs:
#     print(f"\t{name}")
