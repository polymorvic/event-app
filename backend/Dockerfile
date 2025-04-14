FROM python:3.12-alpine

RUN apk add --no-cache --update --quiet dumb-init g++ musl-dev curl

RUN pip install pipenv --no-cache-dir

RUN curl -sL https://taskfile.dev/install.sh | sh -s -- -b /usr/local/bin

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pipenv install

COPY . .

EXPOSE 8000

CMD ["pipenv", "run", "uvicorn", "src.api.routes:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
