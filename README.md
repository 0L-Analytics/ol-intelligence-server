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
3. For Ubuntu/Debian execute run.dev.sh 
```
sh run.dev.sh
```
4. Test the api at **localhost:5004/ping**
5. Test the app at **localhost:3007**

# Useful docker commands
**First build and then run all services defined in docker-compose.yml in background**
```bash
docker compose up -d --build
```
**Enter the db container to make queries directly on db:**
```bash
docker compose exec -it db /bin/sh
/ # su postgres
/ $ plsql "<entire content of DATABASE_URL variable in .env file>"
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
docker compose logs ol-intel-crawler
```
**Get running containers**
```bash
docker ps
```

**Shut down comtainers and remove volumes (e.g. remove db)**
```bash
docker compose down -v
```

## TODOS
See issues

## Branch naming conventions
Two branches are pretty standard and self explanatory, **dev** and **main**. Nobody develops directly on these two branches. dev branch is used to merge all work branches. Testing is done on dev branch and only from dev branch it is allowed to push to main branch.

Working branches are not pushed to Github, unless there is a very good reason for it. One good reason could be two competing technologies that might take each other over at one time in the future.
