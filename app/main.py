import time
from contextvars import ContextVar
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from starlette.background import BackgroundTasks
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from app.applog import _log
from app.helpers import do_something, remove_file
from app.middleware import RequestContextLogMiddleware, RequestLogEventMiddleware
from app.models import Example

app = FastAPI()
app.add_middleware(RequestContextLogMiddleware)
app.add_middleware(RequestLogEventMiddleware)


@app.get("/health")
async def health():
    return JSONResponse({"healthy": True})


@app.post("/")
async def root(example: Example, background_tasks: BackgroundTasks):
    a_temp_file = "/tmp/" + str(uuid4()) + ".txt"
    result = do_something(example, a_temp_file)
    if result:
        background_tasks.add_task(remove_file, a_temp_file)
        return FileResponse(a_temp_file)
    else:
        return {"error": "unable to process example {} = {}".format(example.name, example.value)}
