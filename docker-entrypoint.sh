#!/usr/bin/env bash
set -e

# Optional: run alembic migrations if RUN_MIGRATIONS=yes
if [ "${RUN_MIGRATIONS:-no}" = "yes" ]; then
  echo "Running alembic migrations..."
  alembic upgrade head
fi

exec "$@"
