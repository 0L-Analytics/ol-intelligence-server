# ol-intelligence-server
Providing answers with on-chain and off-chain data.

## Prerequisites
Before running the ol-intelligence-server, make sure:
- Docker is installed. (For Ubuntu: https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)
- Consider making the post installation configuration for Linux users. (https://docs.docker.com/engine/install/linux-postinstall/) 

## Running the ol-intelligence-server (Linux)
1. Clone the repository
```
git clone https://github.com/0L-Analytics/ol-intelligence-server.git
```
2. Navigate to the path that contains the docker-compose.yml file 
```bash
cd /path/to/yml/directory
```
3. For Ubuntu/Debian execute run.dev.sh. Service names as they defined in docker-compose.yml can be specified after the database backup filename, but this is optional.
```
sh run.dev.sh dump_all_121222.gz crawler client api
```
4. Test the api at **localhost:5004/ping**
5. Test the app at **localhost:3007**
5. Test the tools at **localhost:5005/ping**

# Useful docker commands
**First build and then run all services defined in docker-compose.yml in background**
```bash
docker compose up -d --build
```
**Enter the db container to make queries directly on db:**
```bash
docker exec -it ol-intel-db /bin/bash
/ # su postgres
/ $ psql "<entire content of DATABASE_URL variable in .env file>"
viz_dev=# select count(*) from paymentevent;
...
viz_dev=# select tx->'script'->>'function_name' from accounttransaction where address <> 'C906F67F626683B77145D1F20C1A753B';
...
viz_dev=# exit
/ $ exit
/ # exit
```

**Get logs from a container**
```bash
docker logs ol-intel-crawler
```
**Get running containers**
```bash
docker ps -a
```

**Shut down comtainers and remove volumes (e.g. remove db)**
```bash
docker compose down -v
```

**Force remove a comtainers**
```bash
docker rm -f ol-intel-crawler
```

## TODOS
Apply a design like https://vikdiesel.github.io/admin-one-bulma-dashboard/
See issues on github
Define branch naming conventions
Optimize tools container (or merge with crawler or api)


## Branch naming conventions
Two branches are pretty standard and self explanatory, **dev** and **main**. Development is never done directly on these two branches. Work branches are merged to dev branch. Testing is done on dev branch and only from dev branch it is allowed to push to main branch.
