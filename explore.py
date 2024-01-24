import server_templates
import testplans

thread = server_templates.ServerAiohttpBase(testplans.TpMultyDutBase())
thread.start()
thread.join()
