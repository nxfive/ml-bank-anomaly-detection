
from fastapi import FastAPI, HTTPException
from prometheus_client import Counter, Histogram, Gauge
from functools import wraps
import time, psutil

app = FastAPI()

HTTP_STATUS_COUNT = Counter(
    "ml_app_http_responses_total",
    "Total HTTP responses by status",
    ["endpoint", "status"]
)
REQUEST_LATENCY = Histogram(
    "ml_app_request_latency_seconds",
    "Request latency in seconds",
    ["endpoint"]
)
RAM_USAGE = Gauge("ml_app_ram_usage_mb", "RAM usage in MB")
CPU_USAGE = Gauge("ml_app_cpu_usage_percent", "CPU usage percent")


def track_metrics(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        endpoint_name = func.__name__
        status = 200  
        try:
            result = await func(*args, **kwargs)
        except HTTPException as exc:
            status = exc.status_code
            raise
        except Exception:
            status = 500
            raise
        finally:
            REQUEST_LATENCY.labels(endpoint=endpoint_name).observe(time.time() - start)
            HTTP_STATUS_COUNT.labels(endpoint=endpoint_name, status=str(status)).inc()
            RAM_USAGE.set(psutil.virtual_memory().used / 1024 / 1024)
            CPU_USAGE.set(psutil.cpu_percent())

        return result

    return wrapper
