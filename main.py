from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import asyncio
import datetime
import random
import uvicorn
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
import psutil
from starlette.responses import Response
import logging
from logging.handlers import RotatingFileHandler
import os
import sys

# Define Prometheus metrics
REQUESTS = Counter("http_requests_total", "Total HTTP Requests", ["method", "endpoint"])
CPU_USAGE = Gauge("cpu_usage", "CPU Usage Percentage")
MEMORY_USAGE = Gauge("memory_usage", "Memory Usage Percentage")



app = FastAPI()



log_directory = "C:/promtail/logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

log_file = os.path.join(log_directory, "app.log") # Define the path to the log file

handler = RotatingFileHandler(log_file, maxBytes=2000000, backupCount=5) # I have set up File rotating Handler to write logs
logging.basicConfig(handlers=[handler], level=logging.INFO)
logger = logging.getLogger(__name__)


def update_metrics():
    CPU_USAGE.set(psutil.cpu_percent())
    MEMORY_USAGE.set(psutil.virtual_memory().percent)

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    method = request.method
    endpoint = request.url.path
    REQUESTS.labels(method=method, endpoint=endpoint).inc()
    update_metrics()
    response = await call_next(request)
    return response


#You need to expose a special endpoint to expose the metrics on prom sevrer
@app.get("/metrics")
async def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)



LOG_LEVELS = ["INFO", "WARNING", "ERROR", "DEBUG"]
MESSAGES = [
    "User logged in",
    "Database connection established",
    "Payment processed successfully",
    "API request timeout",
    "New order placed",
    "Cache refreshed",
    "User authentication failed",
]




async def generate_logs():
    yield f"{datetime.datetime.utcnow().isoformat()} [INFO] - Log streaming started\n".encode("utf-8")
    
    while True:
        log = f"{datetime.datetime.utcnow().isoformat()} [{random.choice(LOG_LEVELS)}] - {random.choice(MESSAGES)}\n"
        yield log.encode("utf-8")
        logger.info(log.strip())
        await asyncio.sleep(1)  



@app.get("/logs")
async def stream_logs():
    return StreamingResponse(generate_logs(), media_type="text/plain", status_code=200)





if __name__ == "__main__":
    uvicorn.run(app, port=8000, reload=True)

