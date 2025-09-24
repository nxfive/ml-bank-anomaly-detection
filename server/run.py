import os
import warnings

import uvicorn
from fastapi import FastAPI, HTTPException
from prometheus_client import make_asgi_app

from server.app.routers import api
from server.app.routers.metrics import track_metrics

ENV = os.getenv("ENV", "prod")

if ENV != "dev":
    warnings.filterwarnings("ignore")

app = FastAPI()
app.include_router(api.router)


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
    log_level = "debug" if os.getenv("ENV") == "dev" else "warning"
    uvicorn.run(
        app=app, host="0.0.0.0", port=8000, workers=1, reload=False, log_level=log_level
    )
