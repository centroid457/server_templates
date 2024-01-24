import server_templates
import testplans

thread = server_templates.ServerAiohttpBase(testplans.TpMultyDutBase()).run()
# thread.start()
# thread.join()
