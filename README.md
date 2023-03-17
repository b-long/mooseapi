# Moose API

A project template for API building.

### Install tooling

This project depends on `poetry`.  Install poetry as follows:
1. Install `pipx` (`brew install pipx`), read more: https://pypa.github.io/pipx/
2. Install `poetry` (`pipx install poetry`), read more: https://python-poetry.org/

## Install and run using Poetry
Install the application using Poetry:
```
poetry install
```
Run the application:
```
poetry run python -m uvicorn mooseapi.main:app
```
Run the tests:
```
poetry run pytest --cov=mooseapi .
```
## Install and run using pip:
First, use Poetry to create a requirements.txt file:
```
poetry export -f requirements.txt --output requirements.txt
```
Install the application using pip:
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
Run the application:
```
python -m uvicorn mooseapi.main:app
```
Run the tests:
```
python -m pytest --cov=mooseapi .
```
## Interaction
Access the web services:
```
http://127.0.0.1:8000/
```
For graphical interaction, you can use the Swagger UI for our web services:
```
http://127.0.0.1:8000/docs
```
Or ReDoc:
```
http://127.0.0.1:8000/redoc
```
