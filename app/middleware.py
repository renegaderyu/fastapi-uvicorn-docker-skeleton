import time
from contextvars import ContextVar
from uuid import uuid4

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from app.applog import _log

CORRELATION_ID_CTX_KEY = "correlation_id"
REQUEST_ID_CTX_KEY = "request_id"

_correlation_id_ctx_var: ContextVar[str] = ContextVar(CORRELATION_ID_CTX_KEY, default=None)
_request_id_ctx_var: ContextVar[str] = ContextVar(REQUEST_ID_CTX_KEY, default=None)


def get_correlation_id() -> str:
    return _correlation_id_ctx_var.get()


def get_request_id() -> str:
    return _request_id_ctx_var.get()


class RequestContextLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        correlation_id = _correlation_id_ctx_var.set(request.headers.get("X-Correlation-ID", str(uuid4())))
        request_id = _request_id_ctx_var.set(str(uuid4()))

        response = await call_next(request)
        response.headers["X-Correlation-ID"] = get_correlation_id()
        response.headers["X-Request-ID"] = get_request_id()

        _correlation_id_ctx_var.reset(correlation_id)
        _request_id_ctx_var.reset(request_id)

        return response


class RequestLogEventMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        start_time = time.time()
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        formatted_process_time = "{0:.2f}".format(process_time)
        if request.url.path != "/health":
            await _log(
                "access.log",
                method=request.method,
                path=request.url.path,
                host=request.client.host,
                completed_in=formatted_process_time,
                status_code=response.status_code,
                request_id=response.headers["X-Request-ID"],
                correlation_id=response.headers["X-Correlation-ID"],
            )
        return response
