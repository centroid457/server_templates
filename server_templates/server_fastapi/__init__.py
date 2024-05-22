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
from .main import (
    # BASE
    create_app__FastApi,
    create_app__APIRouter,

    # AUX
    DataExample,
    ServerFastApi_Thread,
    start_1__by_terminal,
    start_2__by_thread,
    start_3__by_asyncio,

    # TYPES

    # EXX
)

# =====================================================================================================================
