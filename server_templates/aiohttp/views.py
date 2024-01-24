from aiohttp import web


async def response__index(request):
    msg = """
<!doctype html>
<html lang="en-US">
  <head>
    <meta charset="utf-8" />
    <title>INDEX</title>
    <meta http-equiv="refresh" content="2; url=/" />
  </head>
  <body>
    response__index<br />
    <a href="/start">START</a><br />
    <a href="/stop">STOP</a><br />
  </body>
</html>
    """
    print(msg)
    return web.Response(text=msg, content_type='text/html')


async def response__start(request):
    msg = """
<!doctype html>
<html lang="en-US">
  <head>
    <meta charset="utf-8" />
    <title>INDEX</title>
    <meta http-equiv="refresh" content="1; url=/" />
  </head>
  <body>
    response__start<br />
    <p><a href="/">Redirect</a></p>
  </body>
</html>
    """
    print(msg)
    return web.Response(text=msg, content_type='text/html')


async def response__stop(request):
    msg = """
    <!doctype html>
    <html lang="en-US">
      <head>
        <meta charset="utf-8" />
        <title>INDEX</title>
        <meta http-equiv="refresh" content="1; url=/" />
      </head>
      <body>
        response__stop<br />
        <p><a href="/">Redirect</a></p>
      </body>
    </html>
    """
    print(msg)
    return web.Response(text=msg, content_type='text/html')
