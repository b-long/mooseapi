# Moose Blog

Small blog about Moose.

## Install and run using Poetry
Install the application using Poetry:
```
poetry install
```
Run the application:
```
poetry run python -m uvicorn mooseblog.main:app
```
Run the tests:
```
poetry run pytest --cov=mooseblog .
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
python -m uvicorn mooseblog.main:app
```
Run the tests:
```
python -m pytest --cov=mooseblog .
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
