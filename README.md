# ol-intelligence-server
Providing answers with on-chain and off-chain data.

## Prerequisites
Before running the ol-intelligence-server, make sure:
- Docker is installed. (For Ubuntu: https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)
- Consider making the post installation configuration for Linux users. (https://docs.docker.com/engine/install/linux-postinstall/) 

## Running the ol-intelligence-server (Linux)
1. Clone the repository `git clone https://github.com/0L-Analytics/ol-intelligence-server.git`
2. Navigate to the path that contains the docker-compose.yml file `cd /path/to/yml/directory`
3. Run the following docker compose command: `docker compose up -d --build`. If you have an older version of docker compose installed, you might need to add a hyphen between docker and compose like: `docker-compose up -d --build`

## TODO
- Create data model
- Start loading data
- Source community wallet addresses
- ...
