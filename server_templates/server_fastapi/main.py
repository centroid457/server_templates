from typing import *
from enum import Enum
from PyQt5.QtCore import QThread
import time

from object_info import ObjectInfo
from server_templates.url import UrlCreator

from fastapi import FastAPI, Path, Query, Body, Response
from fastapi.responses import JSONResponse, RedirectResponse

from pydantic import BaseModel
import uvicorn

from starlette import status
from starlette.responses import Response

from logger_aux import Logger


# =====================================================================================================================
class DataExample:
    int = 1
    float = 1.2
    str = "string"
    list = [1, "2"]
    dict = {1: "2", "22": 11}       # by FastAPI return={"1":"2","22":11}


# =====================================================================================================================
def _minimal():
    import uvicorn
    from fastapi import FastAPI, Response
    from fastapi.responses import RedirectResponse

    app = FastAPI()

    @app.get("/")
    async def redirect() -> Response:
        return RedirectResponse(url="/docs")

    @app.get("/{path}")
    async def hello(path):
        print(path)
        return path

    uvicorn.run(app, host="localhost", port=80)


# =====================================================================================================================
def create_app__FastApi(self: Any = None, data: Any = None) -> FastAPI:
    class Item(BaseModel):
        value: int

    # UNIVERSAL ======================================================
    if data is None:
        data = DataExample()

    app = FastAPI()
    app.data = data
    app.LOGGER = Logger("FastAPI").LOGGER

    # WORK -----------------------------------------------------------
    @app.get("/")
    async def redirect() -> Response:
        return RedirectResponse(url="/docs")

    @app.post("/post/dict")
    async def post(item: Item):
        app.LOGGER.debug(item)
        data.dict.update(item)
        print(data.dict)
        return item

    pass
    pass
    pass
    pass
    pass
    pass

    # EXAMPLES =======================================================
    pass

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
        return "FINISH!!!!"     # TODO: FIXME: FINISH!!!

    # PARAMS ----------------------------------------------------------------------------------------------------------
    # VALIDATION ------------------------
    @app.get("/validation/")
    async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):
        results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
        if q:
            results.update({"q": q})
        return results

    # PATH_PARAMS -----------------------------------------------------------
    # chars ----------------------
    @app.get("/path_chars/{name}")
    async def path(name: str):
        """
            http://localhost:8000/path_chars/123 -> "123"

            http://localhost:8000/path_chars/111-222!@$%5E*()_-+=.,%3C%3E%7B%7D[]%60~#CommentFinal  -> "111-222!@$^*()_-+=.,<>{}[]`~"

        COMMENTS = only FINAL!
            http://localhost:8000/path_chars/111-222#CommentFinal/hello     -> "111-222"
        """
        return name

    # order_matters ----------------------
    @app.get("/path_param/fixed")
    async def order_matters():
        return {"path_param": "FIXED PATH PLACE FIRST!"}

    @app.get("/path_param/{as_param}")
    async def order_matters(as_param: str):
        return {"path_param": as_param}

    # UNIVERSAL+NONE_AS_DEFAULT-----------------------------
    @app.get("/path_param_try_def/{name}/{value}")  # path item must used! if not - 404=NOT FOUND
    # def path_params(name, value=None):  # so never use None! -  it would not affect anything!
    async def path_params(name, value):
        """
            http://localhost:8000/path_param_try_def/111/       ->{"detail":"Not Found"}
            http://localhost:8000/path_param_try_def/111/222    ->{"name":"111","value":"222"}
        """
        return {"name": name, "value": value}

    @app.get("/path_params__validate_type/{name}/{value}")
    async def path_params__validate_type(name: str, value: int):
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
    async def params_validate__overload(name: str, value2: str):
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

    # QUERY_PARAMS ------------------------------------------------------------------
    """
    OPTIONAL CORRECT SYNTAX
    ALL YOU NEED IS SET NONE AS DEFAULT VALUE FOR ANY TYPE!!! - Having a default value of any type, including None, makes the parameter optional (not required).
    
    
    FastAPI will know that the value of q is not required because of the default value = None. - SEEMS IT BEST! JUST USE "= NONE"!!!
    The Union in Union[str, None] is not used by FastAPI, but will allow your editor to give you better support and detect errors. - JUST FOR IDE DEBUGGING
        
    Union[str, None] (or str | None in Python 3.10)
        q: str | None = None    - AS BEST IN DOCS!!! for new python!
        q: Union[str, None] = None  - for old python!
    """

    @app.get("/query_chars")
    async def query(q: Union[str, None] = None):
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
    async def query(q1: Union[str, None] = None, q2: Union[str, None] = None):
        """
            http://localhost:8000/query_several?q2=222&q1=111 -> {"q1":"111","q2":"222"}

        comment - only final!
            http://localhost:8000/query_several?q1=123#CommentFinal&q2=willNotUsed -> {"q1":"123","q2":null}

        """
        return {"q1": q1, "q2": q2}

    @app.get("/query_list")
    async def query(
            q: Annotated[Union[list[str], None], Query()] = None,
            q2: Annotated[list[str], Query()] = ["foo", "bar"],
    ):
        """
        To declare a query parameter with a type of list, you need to explicitly use Query, otherwise it would be interpreted as a request body.
            http://localhost:8000/query_list?q=1&q=2    -> {"q":["1","2"]}
            http://localhost:8000/query_list?q=1        -> {"q":["1"]}
            http://localhost:8000/query_list            -> {"q":null}

            http://localhost:8000/query_list            -> {"q":null,"q2":["foo","bar"]}
        """
        return {"q": q, "q2": q2}

    @app.get("/query_with_path/{param}")
    async def query(param: int, q: Union[str, None] = None):
        return {"param": param, "q": q}

    @app.get("/query_validate")
    async def query(q: Union[bool, None] = None, qenum: Model_Enum = None):
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

    @app.get("/query_required")
    async def query(q: str):
        """
        when not passed
            http://localhost:8000/query_required
                -> {"detail":[{"type":"missing","loc":["query","q"],"msg":"Field required","input":null,"url":"https://errors.pydantic.dev/2.6/v/missing"}]}

        when passed
            http://localhost:8000/query_required?q=111  -> {"q":"111"}
        """
        return {"q": q}

    @app.get("/query_optional")
    async def query(q: str = None):
        """
        its enough to set None + not need notice in Annotation!

            http://localhost:8000/query_optional    -> {"q":null}
        """
        return {"q": q}

    # POST ------------------------------------------------------------------------------------------------------------
    """
    To send data, you should use one of: POST (the more common), PUT, DELETE or PATCH.
    Sending a body with a GET request has an undefined behavior in the specifications, nevertheless, it is supported by FastAPI, only for very complex/extreme use cases.
    As it is discouraged, the interactive docs with Swagger UI won't show the documentation for the body when using GET, and proxies in the middle might not support it.
    """

    # MODELS ---------------------------------
    class Item(BaseModel):
        name: str
        description: str | None = None
        price: float
        tax: float | None = None

    class User(BaseModel):
        username: str
        full_name: str | None = None

    @app.post("/post/nobody/start")
    async def post():
        return

    @app.post("/post/body/single/")
    async def post(item: Item | None = None):
        """
        BODY could be Optional!!!

        Expected BODY simple
            {
                "name": "Foo",
                "description": "The pretender",
                "price": 42.0,
                # "tax": 3.2
            }
        """
        # return item

        item_dict = item.dict()
        if item.tax:
            price_with_tax = item.price + item.tax
            item_dict.update({"price_with_tax": price_with_tax})

        if item:
            item_dict.update({"item": item})

        return item_dict

    @app.post("/post/body/multy/")
    async def post(item: Item | None = None, user: User | None = None, extra_singular: Annotated[int | None, Body()] = None):
        """
        Expected BODY as complicated
            {
                "item": {
                    "name": "Foo",
                    "description": "The pretender",
                    "price": 42.0,
                    "tax": 3.2
                },
                "user": {
                    "username": "dave",
                    "full_name": "Dave Grohl"
                },
                "extra_singular": None,
            }
        """
        results = {"item": item, "user": user, "extra_singular": extra_singular}
        return results

    @app.post("/post/all_params/{item_id}")
    async def post(item_id: int, item: Item, q: str | None = None):
        """
        RECOGNITION ORDER!
        The function parameters will be recognized as follows:
            If the parameter is also declared in the path, it will be used as a path parameter.
            If the parameter is of a singular type (like int, float, str, bool, etc) it will be interpreted as a query parameter.
            If the parameter is declared to be of the type of a Pydantic model, it will be interpreted as a request body.
        """
        return {"item_id": item_id, **item.dict(), "q": q}

    # RESPONSE ----------------------------------------------------------------
    @app.get("/redirect")
    async def redirect() -> Response:
        return RedirectResponse(url="https://ya.ru")    # INFO: 127.0.0.1:61637 - "GET /redirect HTTP/1.1" 307 Temporary Redirect

    @app.get("/")
    async def redirect() -> Response:
        return RedirectResponse(url="/docs")

    @app.get("/json")
    async def json() -> Response:
        return JSONResponse(
            content={"message": "Here's your interdimensional portal."},
            status_code=200,
        )

    # RESULT ------------------------------------------------------------------
    return app


# =====================================================================================================================
def create_app__APIRouter() -> 'APIRouter':
    pass

    # from fastapi import APIRouter
    # from starlette import status
    # from starlette.responses import Response

    # from bot import proceed_release
    # from models import Body, Actions
    #
    # api_router = APIRouter()  # noqa: pylint=invalid-name
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
    #
    # return api_router


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
class ServerFastApi_Thread(Logger, QThread):
    """
    WORK IN both LINUX/Win!!!
    """
    PORT: int = 80
    HOST: str = "0.0.0.0"
    # HOST: str = "localhost"
    """
    HOST SETTINGS RULES
    localhost - CANT ACCESS BY HOST_IP! only
        http://localhost/ - OK!
        http://127.0.0.1/ - OK!
        http://192.168.75.140/ - FAIL!!!
    
    0.0.0.0 - ALL ARE OK!!!
        http://localhost/ - OK!
        http://127.0.0.1/ - OK!
        http://192.168.75.140/ - OK!!!
    """

    data: Any = None
    create_app: Callable[[Any], FastAPI] = create_app__FastApi

    @property
    def ROOT(self) -> str:
        return UrlCreator().URL_create(host=self.HOST, port=self.PORT)

    def __init__(self, app: FastAPI = None, data: Any = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if data is None:
            data = self.data

        if app is None:
            app = self.create_app(data=data)
        self.app = app
        self.data = app.data

    def run(self):
        self.LOGGER.debug("run")
        uvicorn.run(self.app, host=self.HOST, port=self.PORT)

    def start(self, *args, **kwargs):
        super().start()
        time.sleep(1)


def start_2__by_thread(app: FastAPI = None) -> Never:
    server = ServerFastApi_Thread(app)
    # server.run()
    server.start()
    server.wait()


# =====================================================================================================================
def start_3__by_asyncio(app: FastAPI) -> Never:
    pass

    # async uvicorn.run(app, host="0.0.0.0", port=8000)


# =====================================================================================================================
# class ServerFastApi__Wrong1(FastAPI, QThread):
#     HOST = "0.0.0.0"
#     PORT = 8000
#
#     DATA = DataExample()
#
#     @get("/data/{attr}")    # EXX
#     def hello(self, attr):
#         return getattr(self.DATA, attr)
#
#     def run(self):
#         uvicorn.run(self, host=self.HOST, port=self.PORT)


# class ServerFastApi__Wrong2(FastAPI, QThread):
#     HOST = "0.0.0.0"
#     PORT = 8000
#
#     DATA = DataExample()
#
#     app = FastAPI()
#
#     def __init__(self, *args, **kwargs):
#         self.add_routs()
#         super().__init__(*args, **kwargs)
#
#     @classmethod
#     def add_routs(cls):               # will not create pathes
#         @cls.app.get("/data/{attr}")
#         async def hello(attr):
#             return getattr(cls.DATA, attr)
#
#     def run(self):
#         uvicorn.run(self, host=self.HOST, port=self.PORT)


# =====================================================================================================================
if __name__ == "__main__":
    start_2__by_thread()


# =====================================================================================================================
