from typing import *
from _aux__release_files import release_files_update


# =====================================================================================================================
VERSION = (0, 0, 3)   # 1/deprecate _VERSION_TEMPLATE from PRJ object +2/place update_prj here in __main__ +3/separate finalize attrs


# =====================================================================================================================
class PROJECT:
    # AUTHOR -----------------------------------------------
    AUTHOR_NAME: str = "Andrei Starichenko"
    AUTHOR_EMAIL: str = "centroid@mail.ru"
    AUTHOR_HOMEPAGE: str = "https://github.com/centroid457/"

    # PROJECT ----------------------------------------------
    NAME_IMPORT: str = "server_templates"
    KEYWORDS: List[str] = [
        "api", "api server", "http server",
        "requests",
        "aiohttp",
        "FastApi",
    ]
    CLASSIFIERS_TOPICS_ADD: List[str] = [
        # "Topic :: Communications",
        # "Topic :: Communications :: Email",
    ]

    # README -----------------------------------------------
    # add DOUBLE SPACE at the end of all lines! for correct representation in MD-viewers
    DESCRIPTION_SHORT: str = "templates for servers"
    DESCRIPTION_LONG: str = """designed for keep all servers templates in one place"""
    FEATURES: List[str] = [
        # "feat1",
        # ["feat2", "block1", "block2"],

        ["[SERVERS]",
            "[aiohttp] (try not to use, as old)",
            "[FastApi] (preferred)",
         ],
        "client_requests item+stack",
    ]

    # HISTORY -----------------------------------------------
    VERSION: Tuple[int, int, int] = (0, 3, 3)
    TODO: List[str] = [
        "...",
    ]
    FIXME: List[str] = [
        "...",
    ]
    NEWS: List[str] = [
        "[clientRequestsItem] fix check_success",

        "[__INIT__.py] fix import",
        "apply last pypi template",
    ]

    # FINALIZE -----------------------------------------------
    VERSION_STR: str = ".".join(map(str, VERSION))
    NAME_INSTALL: str = NAME_IMPORT.replace("_", "-")


# =====================================================================================================================
if __name__ == '__main__':
    release_files_update(PROJECT)


# =====================================================================================================================
