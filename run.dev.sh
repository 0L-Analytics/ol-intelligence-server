#!/bin/sh

echo "copy model.py"
cp -f ./services/datahub/src/crawler/db/model.py ./services/api/src/api/oldata/models.py
cp -f ./services/datahub/src/crawler/db/model.py ./services/tools/src/api/ol/models.py

echo "export REACT_APP_API_SERVICE_URL"
export REACT_APP_API_SERVICE_URL=http://localhost:5004

echo "run docker compose"
if ! command -v docker compose &> /dev/null
then
    docker compose up -d --build
elif ! command -v docker-compose &> /dev/null
then
    docker-compose up -d --build
else
    echo "docker compose not installed?"
    exit
fi

echo "sleep 15 secs"
sleep 15

echo "restore db"
gunzip < ./services/datahub/src/db/dump_all.gz | docker exec -i ol-intel-db psql -U ol_intel -d viz_dev
