FROM python:3.13

WORKDIR /app

RUN apt-get update && apt-get install -y curl && \
    curl -O https://dl.min.io/client/mc/release/linux-amd64/mc && \
    chmod +x mc && mv mc /usr/bin/mc

COPY pyproject.toml poetry.lock ./

RUN pip install poetry && poetry install --no-dev --no-interaction --no-ansi -vvv

COPY ./src /app

RUN mc alias set minio http://minio:9000 minioadmin minioadmin && \
     until mc alias ls minio; do echo "Waiting for MinIO..."; sleep 5; done && \
     mc mb minio/memes || true

ENTRYPOINT ["bash", "-c", "poetry run uvicorn app.main:app --host 0.0.0.0 --port 8001"]
