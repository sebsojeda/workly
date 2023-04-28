# workly

An applicant tracking system (ATS) API. Built using Python, SQLAlchemy, and FastAPI.

## Getting Started

Create a virtual environment

```sh
python -m venv venv
```

Install dependencies

```sh
# don't forget to check that the virutal environment has been activated
pip install -r requirements.txt
```

Start the application for development

```sh
uvicorn workly.main:app --reload
```

## Using the API

You should now be able to interact with and view the API documentation at localhost:8000/docs.
The OpenAPI docs are auto-generated using FastAPI.
