import server_templates
import testplans


server_templates.ServerAiohttp(testplans.TpMultyDutBase()).run()