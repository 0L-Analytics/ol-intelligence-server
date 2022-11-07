#!/bin/sh

echo "copy model.py"

cp -f ./services/datahub/src/crawler/db/model.py ./services/api/src/api/oldata/models.py

echo "export REACT_APP_API_SERVICE_URL"

export REACT_APP_API_SERVICE_URL=http://localhost:5004

echo "run docker compose"

docker compose up -d --build
