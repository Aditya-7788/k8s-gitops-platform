import json
import logging
import os
import signal
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import requests
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "info").upper(),
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger("task-worker")
processed = Counter("tasks_processed_total", "Tasks observed by the worker")
loop_errors = Counter("worker_loop_errors_total", "Worker poll failures")
stopping = threading.Event()
api_url = os.getenv("API_URL", "http://api:8000").rstrip("/")
interval = max(1, int(os.getenv("WORKER_INTERVAL_SECONDS", "10")))


class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            body = b'{"status":"ok"}'
            content_type = "application/json"
        elif self.path == "/metrics":
            body = generate_latest()
            content_type = CONTENT_TYPE_LATEST
        else:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, _format, *_args):
        return


def stop(_signum, _frame):
    stopping.set()


def poll_tasks():
    try:
        response = requests.get(f"{api_url}/tasks", timeout=5)
        response.raise_for_status()
        for task in response.json():
            logger.info("observed task %s", json.dumps(task, sort_keys=True))
            processed.inc()
    except (requests.RequestException, ValueError):
        loop_errors.inc()
        logger.exception("task polling failed")


def main():
    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    server = ThreadingHTTPServer(("0.0.0.0", 8001), MetricsHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    logger.info("worker started; polling %s every %ss", api_url, interval)
    try:
        while not stopping.is_set():
            poll_tasks()
            stopping.wait(interval)
    finally:
        server.shutdown()
        server.server_close()
        logger.info("worker stopped")


if __name__ == "__main__":
    main()
