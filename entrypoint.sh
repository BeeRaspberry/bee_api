#!/usr/bin/env bash

echo "Run DB Upgrade"

flask db upgrade

if [[ ! -z "${DATABASE_DIR}" && ! -f "${DATABASE_DIR}/seed" &&  ! -z "${SEED}" ]]; then
  echo "Run DB Seed"
  flask seed && touch "${DATABASE_DIR}/seed"
fi

/usr/bin/supervisord
flask run --host=0.0.0.0
#gunicorn --chdir app main:app -w 2 --threads 2 -b 0.0.0.0:8000
