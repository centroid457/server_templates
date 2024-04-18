from typing import *
from enum import Enum
from PyQt5.QtCore import QThread

from object_info import ObjectInfo

from fastapi import FastAPI
import uvicorn

from starlette import status
from starlette.responses import Response


# =====================================================================================================================
def create_app__FastApi() -> FastAPI:
    app = FastAPI()

    # NOT FOUND ------------------------------------------------------
    async def NOT_FOUND():
        pass
        # by default if not specified on any resuets return - {"detail": "Not Found"}

    # ORDER ----------------------------------------------------------
    @app.get("/order")
    async def order_1():
        return "ALWAYS WORK FIRST MATCH!!!"

    @app.get("/order")
    async def order_2():
        return "this will work NEVER!!!"

    # CASE_SENSE -----------------------------------------------------
    @app.get("/CASE")
    async def case_sense():
        return "CaseSensitive!!!"

    # SLASHES ---------------------------------------------------------
    # COUNT -----------------
    @app.get("/slash_finish")   # this is another path! '/slash/' and '/slash' - is different!!!
    async def slash_single():
        return {"slash_finish": ""}

    @app.get("/slash_finish/")
    async def slash_single():
        return {"slash_finish": "/"}

    @app.get("/slash_finish//")
    async def slash_double():
        return {"slash_finish": "//"}

    @app.get("/slash_finish///")
    async def slash_triple():
        return {"slash_finish": "///"}

    # START -----------------
    @app.get("/slash")
    async def slash_start():
        return "/slash"

    @app.get("slash")       # never met! so you need use at least one start slash!!!
    async def slash_nostart():
        return "slash"

    @app.get("slash_no")       # never met! even by 'http*.../slash_no'
    async def slash_no():
        return "slash_no"

    # FUNC_NAMES ------------------------------------------------------
    @app.get("/1")
    async def same_name():
        return {"same_name": 1}

    @app.get("/2")
    async def same_name():    # decorator is the unic! name for func is not important!!!
        return {"same_name": 2}

    # TYPES -----------------------------------------------------------
    @app.get("/return_types/str")
    async def return_types():
        return "str"

    @app.get("/return_types/int")
    async def return_types():
        return 123

    @app.get("/return_types/float")
    async def return_types():
        return 111.222

    @app.get("/return_types/true")
    async def return_types():
        return True         # true

    @app.get("/return_types/false")
    async def return_types():
        return False        # false

    @app.get("/return_types/none")
    async def return_types():
        return None         # null

    @app.get("/return_types/list")
    async def return_types():
        return [1,"2",]

    @app.get("/return_types/dict")
    async def return_types():
        return {"key": "value"}

    @app.get("/return_types/model")
    async def return_types():
        """
        You can also return Pydantic models (you'll see more about that later).
        There are many other objects and models that will be automatically converted to JSON (including ORMs, etc). Try using your favorite ones, it's highly probable that they are already supported.
        """
        return "FINISH!!!!" # TODO: FIXME: FINISH!!!

    # PARAMETERS -----------------------------------------------------------
    # order_matters ----------------------
    @app.get("/users/fixed")
    async def order_matters():
        return {"user_id": "FIXED PATH PLACE FIRST!"}

    @app.get("/users/{as_param}")
    async def order_matters(as_param: str):
        return {"user_id": as_param}

    # UNIVERSAL -----------------------------
    @app.get("/path_params/{name}/{value}")  # path item must used! if not - 404=NOT FOUND
    # def path_params(name, value=None):  # so never use None!
    async def path_params(name, value):
        return {"name": name, "value": value}

    @app.get("/path_params__validate_type/{name}/{value}")
    async def path_params__validate_type(name: 'str', value: 'int'):
        """
        VALIDATION will try to change type
        so
            /1 -> int -> 1
            /1 -> str -> "1"
        for error
            /wrong -> int -> {"detail":[{"type":"int_parsing","loc":["path","value"],"msg":"Input should be a valid integer, unable to parse string as an integer","input":"wrong","url":"https://errors.pydantic.dev/2.6/v/int_parsing"}]}

        http://localhost:8000/params_validate/hello/1 -> {"name":"hello","value":1}
        """
        return {"name": name, "value": value}

    @app.get("/params_validate/{name}/{value2}")
    async def params_validate__overload(name: 'str', value2: 'str'):
        """
        OVERLOAD WOULDNOT WORK!!!
        INFO:     127.0.0.1:55128 - "GET /params_validate/hello/wrong HTTP/1.1" 422 Unprocessable Entity
        """
        return {"name": name, "value2": value2}

    # PATH_LONG ----------------------
    @app.get("/files/{file_path:path}")
    async def path_long(file_path: str):
        """
        http://localhost:8000/files/hello/123 -> {"file_path":"hello/123"}
        http://localhost:8000/files//hello/123 -> {"file_path":"/hello/123"}
        """
        return {"file_path": file_path}

    # ENUM ----------------------
    class Model_Enum(str, Enum):    # important define by both STR+ENUM!!!
        alexnet = "alexnet"
        resnet = "resnet"
        lenet = "lenet"

    @app.get("/path_params__validate_enum/{name_by_enum}")
    async def path_params__validate_enum(name_by_enum: Model_Enum):
        if name_by_enum is Model_Enum.alexnet:
            return {"model_name": name_by_enum, "message": "Deep Learning FTW!"}

        if name_by_enum.value == "lenet":
            return {"model_name": name_by_enum, "message": "LeCNN all the images"}

        return {"model_name": name_by_enum, "message": "Have some residuals"}

    # QUERY ------------------------------------------------------------------
    @app.get("/query")
    async def query(q: Union['str', None] = None):
        """
        QUERY params are all that not parametrizes
        The query is the set of key-value pairs that go after the ? in a URL, separated by & characters.

        FOR BLANC - RETURN NULL
            http://localhost:8000/query?        -> {"q":null}
            http://localhost:8000/query?123     -> {"q":null}

            http://localhost:8000/query?q       -> {"q":""}
            http://localhost:8000/query?q=      -> {"q":""}
            http://localhost:8000/query?q=123   -> {"q":"123"}

            http://localhost:8000/query/?q=     -> {"q":""}    # query is not depends on last finishing slash!!!
            http://localhost:8000/query//?q=    -> {"q":""}    # query is not depends on last finishing slash!!!

            http://localhost:8000/query?hello=123 -> {"q":null}     # use not defined query param! - no error!

        try send None
            http://localhost:8000/query?        -> {"q":null}   # seems only one way is not send any!!!
            http://localhost:8000/query?q=null  -> {"q":"null"}
            http://localhost:8000/query?q=none  -> {"q":"none"}
            http://localhost:8000/query?q=None  -> {"q":"None"}

        quotation marks
            http://localhost:8000/query?q="none"    -> {"q":"\"none\""}
            http://localhost:8000/query?q=%22none%22 - past to here by copy from address in brouser!

        simbols
            http://localhost:8000/query?q=\ /_- =[]{}()<>:;,.*!?@$%^~#CommentFinal -> {"q":"\\ /_- =[]{}()<>:;,.*!?@$%^~"}
        """
        return {"q": q}

    @app.get("/query_several")
    async def query(q1: Union['str', None] = None, q2: Union['str', None] = None):
        """
            http://localhost:8000/query_several?q2=222&q1=111 -> {"q1":"111","q2":"222"}

        comment - only final!
            http://localhost:8000/query_several?q1=123#CommentFinal&q2=willNotUsed -> {"q1":"123","q2":null}

        """
        return {"q1": q1, "q2": q2}

    @app.get("/query/{param}")
    async def query(param: 'int', q: Union['str', None] = None):
        return {"param": param, "q": q}

    @app.get("/query_validate")
    async def query(q: Union['bool', None] = None):
        """
        BOOL - any extended convertation!
            http://localhost:8000/query_validate            -> {"q":null}

            http://localhost:8000/query_validate?q=1        -> {"q":true}

            http://localhost:8000/query_validate?q=TRUE     -> {"q":true}
            http://localhost:8000/query_validate?q=True     -> {"q":true}
            http://localhost:8000/query_validate?q=true     -> {"q":true}

            http://localhost:8000/query_validate?q=Y        -> {"q":true}
            http://localhost:8000/query_validate?q=Yes      -> {"q":true}

            http://localhost:8000/query_validate?q=ON      -> {"q":true}

            http://localhost:8000/query_validate?q=0        -> {"q":false}

        BOOL WRONG
            http://localhost:8000/query_validate?q=         -> {"detail":[{"type":"bool_parsing","loc":["query","q"],"msg":"Input should be a valid boolean, ....
            http://localhost:8000/query_validate?q="yes"
        """
        return {"q": q}

    # POST --------------------------------------------------------------------
    @app.post("/post/start")
    async def start():
        return

    # RESULT ------------------------------------------------------------------
    return app


# =====================================================================================================================
def create_app__APIRouter() -> 'APIRouter':
    from fastapi import APIRouter
    from starlette import status
    from starlette.responses import Response

    # from bot import proceed_release
    # from models import Body, Actions
    #
    api_router = APIRouter()  # noqa: pylint=invalid-name
    #
    # @api_router.post("/release/")
    # async def release(*,
    #                   body: Body,
    #                   chat_id: str = None,
    #                   release_only: bool = False):
    #
    #     if (body.release.draft and not release_only) or body.action == Actions.released:
    #         res = await proceed_release(body, chat_id)
    #         return Response(status_code=res.status_code)
    #     return Response(status_code=status.HTTP_200_OK)

    return api_router


# =====================================================================================================================
pass
pass
pass
pass


def start_1__by_terminal(app: FastAPI) -> None:
    """
    uvicorn main:app
    uvicorn main:app --reload

    2=FROM PYTHON CODE
    https://stackoverflow.com/questions/62856818/how-can-i-run-the-fast-api-server-using-pycharm
    """
    pass


# =====================================================================================================================
class ServerFastApi(QThread):
    """
    WORK IN LINUX!!!
    """

    def __init__(self, app: FastAPI, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app

    def run(self):
        uvicorn.run(self.app, host="0.0.0.0", port=8000)


def start_2__by_thread(app: FastAPI) -> Never:
    server = ServerFastApi(app)
    # server.run()
    server.start()
    server.wait()


# =====================================================================================================================
def start_3__by_asyncio(app: FastAPI) -> Never:
    pass

    # async uvicorn.run(app, host="0.0.0.0", port=8000)


def main():
    app = create_app__FastApi()
    start_2__by_thread(app)


# =====================================================================================================================
if __name__ == "__main__":
    main()


# =====================================================================================================================
