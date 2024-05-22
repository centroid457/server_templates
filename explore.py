# DON'T DELETE!
# useful to start smth without pytest and not to run in main script!

from server_templates import ServerAiohttpBase
import pathlib
import time

# =====================================================================================================================
server1 = ServerAiohttpBase()
server1.PORT = 80
server1.start()
server1.wait()

# server2 = server_templates.ServerAiohttpBase()
# server2.start()
# server2.wait()


# =====================================================================================================================
