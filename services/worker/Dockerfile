FROM python:3.12-slim AS dependencies
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1
WORKDIR /build
COPY requirements.txt .
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim AS runtime
ENV PATH="/opt/venv/bin:${PATH}" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    API_URL=http://api:8000 \
    WORKER_INTERVAL_SECONDS=10 \
    LOG_LEVEL=info
RUN groupadd --system app && useradd --system --gid app --home-dir /app app
WORKDIR /app
COPY --from=dependencies /opt/venv /opt/venv
COPY --chown=app:app worker.py .
USER app
EXPOSE 8001
STOPSIGNAL SIGTERM
CMD ["python", "worker.py"]
