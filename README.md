# unit_commitment

Deploying a unit commitment solution via fastapi

## Development Requirements

- Python3.10.0
- Pip
- Poetry (Python Package Manager)
- Docker 

## Installation

```sh
python3.10 -m venv venv
source venv/bin/activate
make install
```

## Runnning Localhost

To run the application locally without Docker, you can use the following steps:

1. Activate Virtual Environment: If you haven't already, activate your virtual environment.

```sh
source venv/bin/activate
```
2. Install dependencies
```sh
make install
```

3. Run the Application: Use the make run command to start the FastAPI application. 
```sh
make run
```
4. Swagger UI: Once the application is running, you can navigate to http://localhost:8888/docs to access the Swagger UI for API documentation and testing.

## Deploy app

To deploy the application using Docker, you need to simply run `make deploy` and navigate to 
`http://localhost:8888/docs` for the Swagger UI.

When winding down, you can use `make down` to close the container

## Running Tests

`make test`

## Access Swagger Documentation

> <http://localhost:8888/docs>

## Project structure

Files related to application are in the package `unit_commitment` or `tests` directories.
Application parts are:

.
├── Dockerfile
├── Makefile
├── README.md
├── docker-compose.yml
├── notebooks
├── poetry.lock
├── pyproject.toml
├── tests
│   ├── conftest.py
│   ├── test_dummy.py
│   ├── test_greedy.py
│   └── test_production_plan.py
└── unit_commitment
    ├── __init__.py
    ├── api
    │   ├── __init__.py
    │   └── routes
    ├── app.py
    ├── core
    │   ├── __init__.py
    │   ├── config.py
    │   └── logging.py
    ├── production_plan
    │   ├── __init__.py
    │   ├── calculate_production_plan.py
    │   ├── dummy.py
    │   └── greedy.py
    ├── pydantic_models.py
    └── run_app.py