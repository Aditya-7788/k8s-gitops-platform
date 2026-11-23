import os
import time
from itertools import count
from typing import Annotated

from fastapi import FastAPI, Request, Response
from pydantic import BaseModel, Field
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

app = FastAPI(title="Task Manager API")
request_count = Counter(
    "http_requests_total", "HTTP requests", ("method", "path", "status")
)
request_duration = Histogram(
    "http_request_duration_seconds", "HTTP request duration", ("method", "path")
)
errors = Counter("errors_total", "HTTP 5xx responses and unhandled errors")
tasks: list[dict[str, object]] = []
task_ids = count(1)


class TaskInput(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=200)]


@app.middleware("http")
async def instrument_requests(request: Request, call_next):
    if request.url.path == "/metrics":
        return await call_next(request)
    started = time.perf_counter()
    status = 500
    try:
        response = await call_next(request)
        status = response.status_code
        return response
    except Exception:
        raise
    finally:
        path = request.url.path
        request_count.labels(request.method, path, str(status)).inc()
        request_duration.labels(request.method, path).observe(
            time.perf_counter() - started
        )
        if status >= 500:
            errors.inc()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/tasks")
async def list_tasks():
    return tasks


@app.post("/tasks", status_code=201)
async def create_task(task: TaskInput):
    created = {"id": next(task_ids), "title": task.title, "completed": False}
    tasks.append(created)
    return created


@app.get("/load")
async def load():
    deadline = time.perf_counter() + 0.5
    value = 0
    while time.perf_counter() < deadline:
        value = (value * 33 + 17) % 1_000_003
    return {"status": "ok", "work": value}


@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/")
async def root():
    return {"service": "task-manager-api", "environment": os.getenv("APP_ENV", "local")}
