FROM python:3.13

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry && poetry install --no-dev --no-interaction --no-ansi -vvv

COPY ./src /app
COPY alembic.ini /app
COPY ./migrations /app/migrations

RUN poetry run alembic revision --autogenerate -m "Initial migrations" || True

RUN poetry run alembic upgrade head || True

ENTRYPOINT ["bash", "-c", "poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000"]