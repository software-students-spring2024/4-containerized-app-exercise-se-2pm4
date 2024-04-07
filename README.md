![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)

# Containerized App Exercise

Build a containerized app that uses machine learning. See [instructions](./instructions.md) for details.

## Instructions for setting up database

These instructions will guide you through the process of pulling a Docker image from Docker Hub and creating a container from it. To ensure that groupmates are working on the same database instance, the container_name, port_number, username, password should be the same among groupmates.


1. Open a terminal or command prompt.
2. Run the following command to pull the Docker image from Docker Hub:

    ```
    docker pull minjae07206/se2pm4-database
    ```
    
3. Run the following command to create a new container from the image that was pulled. Replace <container_name> and <port_number> with your choice. The username and password can be changed as well.

    ```
    docker run --name <container_name> -v ~/data:/data/db -p <port_number>:27017 -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=secret -d minjae07206/se2pm4-database:latest
    ```
4. Run the following command to exectue the container. Again, replace the <container_name> with the name that was used for container creation in step 3.
    ```
    docker exec -ti <container_name> bash
    ```
5. Run the command to start mongosh. Change the username and password may be changed.
    ```
    mongosh -u admin -p secret
    ```
6. 
    ```
    show dbs
    ```
7. If "test" is in the list of dbs, the database has been successfully installed. You can run mongodb commands to execute CRUD operations. The name of the collection used is imgdata.
    ```
    db.imgdata.find()
    ```
