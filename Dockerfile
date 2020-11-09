FROM python:3.7

COPY ./app /app
COPY ./tests /tests
COPY pyproject.toml poetry.lock ./

RUN apt-get update && \
	apt-get install libdmtx0b && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9980"]

EXPOSE 9980