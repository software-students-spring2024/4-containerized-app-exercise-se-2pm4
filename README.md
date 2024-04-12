![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)

# Containerized App Exercise

Build a containerized app that uses machine learning. See [instructions](./instructions.md) for details.
## Project Overview 

This project consists of 3 parts: machine-learning client, web-app, and database. A user can upload photos in the web-app and view the emotion of the image which is processed by the machine-learning client. 

## Teammates participating in this project

1. Brendan Tang: [Github profile](https://github.com/Tango117)
2. Joseph Lee: [Github profile](https://github.com/pastuhhhh)
3. Minjae Lee: [Github profile](https://github.com/minjae07206)
4. Yiwei Luo: [Github profile](https://github.com/yl7408)

## Instructions to run this project

### Prerequisites & Disclaimers: 
- This project requires the user to download docker. If you have not made an account or downloaded docker, you can do it [here](https://www.docker.com/products/docker-desktop/).
- The `docker-compose.yml` file has environment variables hidden in a `.env` file. Either request the `.env` file from the developer or create your own `.env` file and include variables. All variables inside ${} are variables coming from the .env file. The `.env` file must be placed in the same directory(the root directory) as the `docker-compose.yml`.
- All images are stored locally. There is no need to import any starter data into the database.


### Running the project in 3 docker containers

1. Open the terminal and direct to the root directory of the project. Then, run the command below. 
```
docker-compose up -d --build
```
`up` command is to create and start containers based on the configuartions specified in the `docker-compose.yml` file.
`-d` flag is the detached mode, it starts the containers in the background.
`--build` flag builds any image in the `docker-compose.yml` file if it has not been built already.

2. After all the containers start(might take a while), the user can head to [localhost:5000](http://localhost:5000/) in a browser, to view the web-app where the user can capture photos and upload them. 

3. Once a user uploads the photo, the user can click on the "gallery" button to see the image emotion results. The machine learning client does not have a backend, so runs every 30 seconds to check if there are images that have not been processed and processes them. Therefore, it can take a maximum of 30 seconds to see the image emotion result. 

4. If the user wishes to manually do CRUD operations on the database, read the section on "Managing the Database" below.

5. When the user is done with the application, run the command below to stop all the containers.

```
docker-compose down
```

### Managing the Database

1. The access the MongoDB data, first run:

```
docker exec -it mongodb_server bash
```

2. The command above will open a bash shell inside the mongodb_server container. Then run the command below. The <username> and <password> are inside the `.env`, indicated by `MONGO_INITDB_ROOT_USERNAME` and `MONGO_INITDB_ROOT_PASSWORD`.

```
mongosh -u <username> -p <password>
```

3. The command above will open a mongodb shell. First, switch to the database that is used: the <database_name> is also in the `.env` file, indicated by `MONGO_DB`

```
use <database_name>
```

4. Finally, the user can find the collection inside the database and run CRUD commands. `images` is the name of the collection where data is stored. Here is a example command.

```
db.images.find()
```




