import pathlib
import time
from fastapi import FastAPI, Request
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from starlette_exporter import PrometheusMiddleware, handle_metrics

from mlservefast.api import mlservefast, info
from mlservefast.api.middlewares.errors import catch_exceptions_middleware
from mlservefast.config import GCONFIG

app = FastAPI()


def _create_tmp_dir():
    pathlib.Path(GCONFIG.mlservefast["tmp_dir"]).mkdir(parents=True, exist_ok=True)
    pathlib.Path(GCONFIG.mlservefast["prometheus_dir"]).mkdir(
        parents=True, exist_ok=True
    )


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


_create_tmp_dir()
app.add_middleware(PrometheusMiddleware, app_name="mlservefast")
app.add_middleware(ProxyHeadersMiddleware)
app.add_route("/metrics", handle_metrics)
app.middleware("http")(catch_exceptions_middleware)
app.include_router(info.router)
app.include_router(mlservefast.router)
