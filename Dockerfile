FROM node:16-bullseye AS frontend

RUN mkdir src

WORKDIR /src
COPY package.json .
COPY yarn.lock .
RUN yarn install

COPY . .
RUN yarn run build

FROM python:3.10-bullseye

RUN apt-get update
RUN apt-get install -y yarn python3-pip
RUN pip install poetry

RUN mkdir app
COPY api/pyproject.toml app/
COPY api/poetry.lock app/

WORKDIR /app
RUN poetry install

COPY --from=frontend /src/dist /dist
COPY api .

EXPOSE 8080

CMD [ "poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80" ]
