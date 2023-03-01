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

