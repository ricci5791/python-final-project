FROM python:3.9
COPY /film_api .
COPY poetry.lock .
COPY pyproject.toml .

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8080", "film_api:app"]