# =====================================================================================================================
# VERSION = (0, 0, 1)   # use import EXACT_OBJECTS! not *
#   from .main import *                 # INcorrect
#   from .main import EXACT_OBJECTS     # CORRECT


# =====================================================================================================================
# TEMPLATE
# from .main import (
#     # BASE
#     EXACT_OBJECTS,
#
#     # AUX
#
#     # TYPES
#
#     # EXX
# )
# ---------------------------------------------------------------------------------------------------------------------
from .url import (
    # BASE
    UrlCreator,

    # AUX

    # TYPES

    # EXX
)
from .client_requests import (
    # BASE
    Client_RequestItem,
    Client_RequestsStack,

    # AUX
    ResponseMethod,

    # TYPES
    TYPE__RESPONSE,
    TYPE__REQUEST_BODY,

    # EXX
)

# ---------------------------------------------------------------------------------------------------------------------
from .server_aiohttp import *
from .server_fastapi import *


# =====================================================================================================================
