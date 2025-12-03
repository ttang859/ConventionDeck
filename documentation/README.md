# ConventionDeck
A centralized platform for card convention shows to be hosted, attended and organized.

See<a href="PROJECT_SPECIFICATIONS.md"> Project Specifications </a>for more details on **Project Description** and **Architecture Overview**

## Prerequistes:
- Docker
- Docker Compose
- Python 3.11 or higher

## Installation and Setup
- Open Docker Desktop and have the engine running
- cd into the root directory in terminal (should be named ```\ConventionDeck```)
- To start up the system, run ```docker-compose up -d``` to run the Docker Compose file detached
    - To verify that services are up and running, run ```docker-compose ps``` to see the running containers and health status
- To stop and shut down the system, run ```docker-compose down```

## Usage Instructions:
- ```curl -f http://localhost:8000/health```
- running the installation and setup will trigger automatic health checks from each of the services and their respective dependencies

## API Documentations:
- ```user-service:8000/health:```
    ~~~
    {
        service: user-service,
        status: healthy
        dependencies:
            convention-service:
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
                {
                    redis:{
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
    ~~~
## Testing:
- verify via ```docker-compose ps```

## Project Structure:
- ```\documentation``` has all of the markdown files and diagrams for project details
- ```\...-service``` is a service directory that holds logic for a named microservice. each has its own ```main.py``` file, a ```Dockerfile```, a ```requirements.txt``` file, and a ```models.py``` file
- ```docker-compose.yml``` contains the layout and structure to properly orchestrate this entire system
