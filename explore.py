# import server_templates
# import testplans
# thread = server_templates.ServerAiohttpBase(testplans.TpMultyDutBase()).run()


# ====================================
from setuptools import find_packages

for name in find_packages("server_templates"):
    print(name)
