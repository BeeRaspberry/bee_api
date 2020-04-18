#!/usr/bin/env bash

export FLASK_ENV=development

echo "Run DB Upgrade"

flask db upgrade

if [[ ! -z "${DATABASE_DIR}" && ! -f "${DATABASE_DIR}/seed" &&  ! -z "${SEED}" ]]; then
  echo "Run DB Seed"
  flask seed && touch "${DATABASE_DIR}/seed"
fi

/usr/bin/supervisord
flask run --host=0.0.0.0
