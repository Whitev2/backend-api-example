#!/bin/bash
# turn on bash's job control
set -m

alembic revision --autogenerate -m "init"
alembic upgrade head
# API
python3 __main__.py