# ConventionDeck
A centralized platform for card convention shows to be hosted, attended and organized.

See<a href="PROJECT_SPECIFICATIONS.md"> Project Specifications </a>for more details on **Project Description** and **Architecture Overview**

## Prerequistes:
- Docker
- Docker Compose
- Python 3.11 or higher

## Installation and Setup
- Open Docker Desktop and have the engine running
- Make sure to move this into a working dev environment (working in the class dev environment)
- cd into the root directory in terminal (should be named ```\ConventionDeck```)
- set up a .env file at the root with:
~~~
USER_DB= user
USER_USER= useruser
USER_PASSWORD= userpass

INV_DB= inventory
INV_USER= inventoryuser
INV_PASSWORD= inventorypass

CONV_DB= convention
CONV_USER= conventionuser
CONV_PASSWORD= conventionpass

PG_PORT= 5432

NUM_DUPES= 2
~~~
- To start up the system, run ```docker-compose up -d``` to run the Docker Compose file detached
    - To verify that services are up and running, run ```docker-compose ps``` to see the running containers and health status
- To stop and shut down the system, run ```docker-compose down```

## Testing:
- Inside ```\test_scripts``` there are several bash scripts to run that test each individual service
- To run:
    - Make sure you are ```cd``` into the root directory
    - ```chmod +x test_scripts/test_{service name}.sh``` to make the script executible
    - Execute ```./test_scripts/test_{service name}.sh``` in the terminal and see results printed out
    - Verify with the ```/test_data``` files and JSON Request Body in the bash scripts to see the intended results

<!-- ## API Documentations:
- ```user-service:8000/health:```
    ~~~
    {
        service: user-service,
        status: healthy
        dependencies:
            inventory-service:
                status: healthy
                response_time_ms: 15
            registration-service:
                status: healthy
                response_time_ms: 15
            userdb:
                status: healthy
                response_time_ms: 15
    }
    ~~~
- ```convention-service:8000/health:```
    ~~~
    {
        service: convetion-service,
        status: healthy
        dependencies:
            [
                {
                    registration-service:{
                        status: healthy
                        response_time_ms: 15
                    }
                }
                {
                    booth-service:{
                        status: healthy
                        response_time_ms: 15
                    }
                }
            ]
    }
    ~~~
- ```registration-service:8000/health:```
    ~~~
    {
        service: registration-service,
        status: healthy
        dependencies:
            redis:
                status: healthy
                response_time_ms: 15
    }
    ~~~
- ```booth-service:8000/health:```
    ~~~
    {
        service: booth-service,
        status: healthy
        dependencies:
            redis:
                status: healthy
                response_time_ms: 15
    }
    ~~~
- ```inventory-service:8000/health:```
    ~~~
    {
        service: inventory-service,
        status: healthy
        dependencies:
            redis:
                status: healthy
                response_time_ms: 15
    }
    ~~~ -->

## Project Structure:
- ```\documentation``` has all of the markdown files and diagrams for project details
- ```\...-service``` is a service directory that holds logic for a named microservice. each has its own ```main.py``` file, a ```Dockerfile```, a ```requirements.txt``` file, and a ```models.py``` file
- ```docker-compose.yml``` contains the layout and structure to properly orchestrate this entire system
