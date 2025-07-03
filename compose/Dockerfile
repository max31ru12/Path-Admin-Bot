FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

ADD https://astral.sh/uv/install.sh /uv-installer.sh

RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /bot

COPY entrypoint.sh .
COPY ../pyproject.toml .
COPY ../uv.lock .
COPY ../app ./app

RUN uv sync --locked

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
