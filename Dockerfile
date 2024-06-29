FROM python:3.11-buster

RUN pip install poetry==1.4.2

WORKDIR /backend

COPY pyproject.toml poetry.lock ./

RUN poetry install --without dev

COPY app ./app


CMD ["poetry", "run", "uvicorn", "app.main:app", "--port", "8000"]