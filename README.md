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
3. Run the following docker compose command:
```sh
docker compose up -d --build
```

   If you have an older version of docker compose installed, you might need to add a hyphen between docker and compose like:

```sh
docker-compose up -d --build
```

## Useful docker commands
### Enter the db container to make queries directly on db:
```bash
docker compose exec -it db /bin/sh
/ # su postgres
/ $ plsql "<entire content of DATABASE_URL variable in .env file>"
viz_dev=# select count(*) from paymentevent;
...
viz_dev=# exit
/ $ exit
/ # exit
```

## TODOS
See issues

## Branch naming conventions
Two branches are pretty standard and self explanatory, **dev** and **main**. Nobody develops directly on these two branches. dev branch is used to merge all work branches. Testing is done on dev branch and only from dev branch it is allowed to push to main branch.

Working branches are not pushed to Github, unless there is a very good reason for it. One good reason could be two competing technologies that might take each other over at one time in the future.

## End-point examples for 0l-explorer api
Base URI is **https://0lexplorer.io/api/**

**/proxy/node/account-transactions**

https://0lexplorer.io/api/proxy/node/account-transactions?address=C906F67F626683B77145D1F20C1A753B&start=1&limit=1000

**/proxy/node/events**

https://0lexplorer.io/api/proxy/node/events?address=C906F67F626683B77145D1F20C1A753B&start=12000&limit=1000

**/webmonitor/vitals**

https://0lexplorer.io/api/webmonitor/vitals

**/proofs (Internal Server Error)**

https://0lexplorer.io/api/proofs/C906F67F626683B77145D1F20C1A753B

**/proxy/node/epoch-events (NOT WORKING)**

https://0lexplorer.io/api/proxy/node/epoch-events?address=C906F67F626683B77145D1F20C1A753B

## End-points for permission-tree api
The permission-tree api docs can be found [here](https://github.com/0L-Analytics/permission-tree-monitoring). The base URI for this api is **https://0lexplorer.io:444**.

Example

**/permission-tree/stats**

https://0lexplorer.io:444/permission-tree/stats
