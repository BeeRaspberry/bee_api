#!/usr/bin/env sh

echo "Run db upgrade and initialize db"
flask db upgrade && flask initdb

if [[ ! -f "${DATABASE_DIR}/seed" &&  ! -z "$SEED" ]]; then
  flask seed && touch "${DATABASE_DIR}/seed"
fi

flask run --host=0.0.0.0
