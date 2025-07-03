FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

RUN pip install poetry

ENV PATH="/root/.local/bin/:$PATH"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /bot

COPY pyproject.toml poetry.lock alembic.ini ./
COPY compose/entrypoint.sh ./

RUN poetry install --no-root

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
