#!/usr/bin/env sh

# Let the DB start
sleep 10;

export FLASK_ENV=development

echo "Run db upgrade"
flask db upgrade

if [[ ! -f "${DATABASE_DIR}/seed" &&  ! -z "$SEED" ]]; then
  flask seed && touch "${DATABASE_DIR}/seed"
fi
