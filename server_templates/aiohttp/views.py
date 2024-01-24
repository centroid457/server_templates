from aiohttp import web


async def response__index(request):
    msg = """
response__index<br />
<a href="/start/">START</a><br />
<a href="/stop/">STOP</a><br />
"""
    print(msg)
    return web.Response(body=msg)


async def response__start(request):
    msg = 'response__start'
    print(msg)
    return web.Response(text=msg)


async def response__stop(request):
    msg = 'response__stop'
    print(msg)
    return web.Response(text=msg)
