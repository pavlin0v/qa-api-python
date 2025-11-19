#!/bin/bash
set -e

echo "Запускаем миграции"
alembic upgrade head

exec "$@"