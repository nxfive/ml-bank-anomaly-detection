import uvicorn
from fastapi import FastAPI, Response
from prometheus_client import make_asgi_app

from server.app.routers import api, metrics

import os

app = FastAPI()
app.include_router(api.router)


if os.getenv("ENV") == "dev":

    @app.get("/error500")
    @metrics.track_metrics
    async def error500():
        raise RuntimeError("Test 500 error")

    @app.get("/error400")
    @metrics.track_metrics
    async def error400():
        return Response(content="Bad Request", status_code=400)


metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


if __name__ == "__main__":
    uvicorn.run(
        app=app, host="0.0.0.0", port=8000, workers=1, reload=False, log_level="info"
    )
