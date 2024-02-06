import server_templates
import pathlib
import time


server = server_templates.ServerAiohttpBase()
server.start()
server.wait()
