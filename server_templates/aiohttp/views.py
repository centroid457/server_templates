from aiohttp import web


async def response__simplest_text(request):
    msg = 'Hello response__simplest_text!'
    print(msg)
    return web.Response(text=msg)
