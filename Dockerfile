FROM python:3.11-slim-bookworm

WORKDIR /app
# Copy only dependency metadata first to leverage Docker cache
COPY pyproject.toml poetry.lock* /app/

RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --only main --no-root

COPY data /app/data
COPY scanner /app/scanner
ENTRYPOINT ["python", "-m", "scanner.cli"]