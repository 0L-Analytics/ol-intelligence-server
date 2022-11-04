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