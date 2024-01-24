import server_templates
import testplans


tpgui = testplans.TpGui()
server_templates.ServerAiohttp(tpgui.DATA).run()
