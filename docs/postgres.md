# Docker
## Handy docker commands
### Backup a db to this project directory
```sh
docker exec -t ol-intel-db mkdir /var/lib/postgresql/backups
docker exec -t ol-intel-db pg_dumpall -c -U ol_intel | gzip > ./services/datahub/src/db/dump_full.gz
```
### Restore the db from this project directory
```sh
gunzip < ./services/datahub/src/db/dump_full.gz | docker exec -i ol-intel-db psql -U ol_intel -d viz_dev
```
