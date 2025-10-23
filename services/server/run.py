import time
from typing import Callable

import uvicorn
from fastapi import FastAPI, HTTPException, Request, Response
from prometheus_client import make_asgi_app

from services.server.app.routers import api
from services.server.app.routers.metrics import track_metrics
from src.utils.logger import logger
from src.utils.settings import settings


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(api.router)
    app.middleware("http")(log_requests)
    
    if settings.ENV == "dev":
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

    @app.get("/health")
    def health_check():
        return {"status": "ok"}

    return app


async def log_requests(request: Request, call_next: Callable) -> Response:
    """
    Log HTTP requests with method, URL, status, duration, and client info.
    """
    start = time.time()
    client_host = request.client.host if request.client else "unknown"

    try:
        response = await call_next(request)
        status_code = response.status_code
    except Exception:
        status_code = 500
        raise
    finally:
        duration = round(time.time() - start, 3)
        log_data = {
            "method": request.method,
            "url": str(request.url),
            "status": status_code,
            "duration": duration,
            "client": client_host,
        }
        if status_code >= 500:
            logger.error("HTTP request failed", extra=log_data)
        else:
            logger.info("HTTP request", extra=log_data)

    return response


if __name__ == "__main__":
    app = create_app()
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        workers=1,
        reload=False,
        log_level=settings.FASTAPI_LOG_LEVEL,
        log_config=None,
        use_colors=False,
        access_log=False,
    )
