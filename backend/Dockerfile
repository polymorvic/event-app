FROM python:3.14-alpine

RUN apk add --no-cache --update --quiet dumb-init g++ musl-dev curl

RUN pip install pipenv --no-cache-dir

RUN curl -sL https://taskfile.dev/install.sh | sh -s -- -b /usr/local/bin

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pipenv install

COPY . .

EXPOSE 8080

CMD ["pipenv", "run", "uvicorn", "fastapi:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
