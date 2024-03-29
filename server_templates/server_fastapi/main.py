from PyQt5.QtCore import QThread



# from typing import Union
#
# from fastapi import FastAPI
#
# app = FastAPI()
#
#
# @app.get("/")
# def read_root():
#     return {"Hello": "World"}
#
#
# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}
#
# input("hello")


# 2 ---------------------------------
# from fastapi import APIRouter
# from starlette import status
# from starlette.responses import Response
#
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
#     if (body.release.draft and not release_only) \
#             or body.action == Actions.released:
#         res = await proceed_release(body, chat_id)
#         return Response(status_code=res.status_code)
#     return Response(status_code=status.HTTP_200_OK)


# 3 ----------------------------------
import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}


# START SERVER --------------------------
# 1=FROM TERMINAL
# uvicorn main:app
# uvicorn main:app --reload

# 2=FROM PYTHON CODE
# https://stackoverflow.com/questions/62856818/how-can-i-run-the-fast-api-server-using-pycharm

class ServerFastApi(QThread):
    def run(self):
        uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    server = ServerFastApi()
    # server.run()
    server.start()
    server.wait()
