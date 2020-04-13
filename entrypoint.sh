#!/usr/bin/env sh

export FLASK_ENV=development

echo "Run db upgrade"
flask db upgrade

if [[ ! -f "${DATABASE_DIR}/seed" &&  ! -z "$SEED" ]]; then
  flask seed && touch "${DATABASE_DIR}/seed"
fi

#/usr/bin/supervisord
#flask run --host=0.0.0.0
