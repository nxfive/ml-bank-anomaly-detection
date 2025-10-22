import os
import time
import warnings

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from prometheus_client import make_asgi_app

from server.app.routers import api
from server.app.routers.metrics import track_metrics
from src.utils.logger import get_logger, setup_logging

setup_logging()
logger = get_logger("main")


ENV = os.getenv("ENV", "dev")

if ENV != "dev":
    warnings.filterwarnings("ignore")

app = FastAPI()
app.include_router(api.router)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = round(time.time() - start, 3)

    logger.info(
        "HTTP request",
        extra={
            "method": request.method,
            "url": str(request.url),
            "status": response.status_code,
            "duration": duration,
            "client": request.client.host,
            "endpoint": (
                request.scope.get("endpoint").__name__
                if request.scope.get("endpoint")
                else None
            ),
        },
    )
    return response


@app.get("/health")
def health_check():
    return {"status": "ok"}


if ENV == "dev":

    @app.get("/error500")
    @track_metrics
    async def error500():
        raise RuntimeError("Test 500 error")

    @app.get("/error400")
    @track_metrics
    async def error400():
        raise HTTPException(status_code=400)


metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


if __name__ == "__main__":
    log_level = "debug" if os.getenv("ENV") == "dev" else "info"
    uvicorn.run(
        app=app, host="0.0.0.0", port=8000, workers=1, reload=False, log_level=log_level
    )
