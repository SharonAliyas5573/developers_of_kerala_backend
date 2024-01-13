FROM python:3.11.0

ENV PYTHONUNBUFFERED 1

WORKDIR /

COPY poetry.lock pyproject.toml ./
RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false

ARG DEV=false
RUN if [ "$DEV" = "true" ] ; then poetry install ; else poetry install --no-dev --no-root ; fi

COPY . .

ENV PYTHONPATH "${PYTHONPATH}:/"

EXPOSE 8080
CMD uvicorn app.main:app --host 0.0.0.0 --port 8080