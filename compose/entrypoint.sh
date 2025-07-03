#!/usr/bin/bash

export PYTHONPATH=/bot

poetry run alembic upgrade head

poetry run python3 app/main.py
