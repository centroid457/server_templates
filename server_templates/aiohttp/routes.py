from typing import *
import pathlib

from .views import *


# =====================================================================================================================
PROJECT_ROOT = pathlib.Path()


# =====================================================================================================================
ROUTES_STATIC: Dict[str, Callable] = {
}

ROUTES_GET: Dict[str, Callable] = {
    '/': response__index,
    '/start': response__start,
    '/stop': response__stop,
}


# =====================================================================================================================
def setup_routes(app):
    for route, response in ROUTES_STATIC.items():
        app.router.add_static(
            route,
            path=PROJECT_ROOT / 'static'
            # name='static'
        )

    for route, response in ROUTES_GET.items():
        app.router.add_get(route, response)


# =====================================================================================================================
