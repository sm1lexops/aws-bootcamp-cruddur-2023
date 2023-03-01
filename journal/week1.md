# Week 1 — App Containerization

## Class Summary Tasks

### Run Python Localy

```sh
cd backend-flask
export FRONTEND_URL="*"
export BACKEND_URL="*"
pip3 install -r requirements.txt
python3 -m flask run --host=0.0.0.0 --port=4567
cd ..
```

> You should see something like this

![Local Run App](assets/run_app_local_cli.jpg)

> Go `PORTS` tab and link to the port 4567

![Local 404](assets/run_app_local.jpg)

- After appent to the url to `/api/activities/home`

> You should get back srv backend `json` answer 

![JSON](assets/run_app_local_with_api.jpg)

## Add to Dockerfile

```sh
FROM python:3.10-slim-buster

WORKDIR /backend-flask

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_ENV=development
ENV FRONTEND_URL=`https://3000-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}`
ENV BACKEND_URL=`https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}`

EXPOSE ${PORT}

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=4567" ]
```

## Build Container

```sh
docker build -t backend-flask ./backend-flask # build container with name `backend-flask`
```

> You should get something like this status

```sh
Successfully built cdd5c72cf552
Successfully tagged backend-flask:latest
```

## Run Container

```sh
docker run --rm -it -p 4567:4567 backend-flask # run container backend-flask in interaction mode, listen port 4567, after `ctrl+C` container will be deleted automaticly
```

> At the end of output you should see

```sh
192.168.34.200 - - [01/Mar/2023 15:24:47] "GET / HTTP/1.1" 404 -
192.168.34.200 - - [01/Mar/2023 15:25:08] "GET /api/activities/home HTTP/1.1" 200 -
```

### Get Running Container ID 

```sh
docker ps -a # `"-a"` argument meaning info about `all` container running and stoped
CONTAINER ID   IMAGE           COMMAND                  CREATED         STATUS         PORTS                                       NAMES
99461a672215   backend-flask   "python3 -m flask ru…"   6 minutes ago   Up 6 minutes   0.0.0.0:4567->4567/tcp, :::4567->4567/tcp   fervent_kirch
```

### Get Container backend json 

- open the link for 4567 in your browser again
- append to the url to /api/acivities/home

> You should get back json like this

![JSON Container](assets/container_app_api.jpg)

### Put Container ID into an Environment Variable

```sh
CONTAINER_ID=$(docker ps -aq)
```

### Send curl to Test Server

```sh
curl -X GET http://localhost:4567/api/activities/home -H "Accept: application/json" -H "Content-Type: application/json"
```

> You'll get same json answer

### You Can Get Container Logs

```sh
docker logs CONTAINER_ID -f
docker logs backend-flask -f
docker logs $CONTAINER_ID -f
```

