FROM 446273730290.dkr.ecr.eu-central-1.amazonaws.com/cruddur-python:3.10-slim-buster

WORKDIR /backend-flask

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

#ENV FRONTEND_URL=`https://3000-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}`
#ENV BACKEND_URL=`https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}`
#ENV FRONTEND_URL="https://omgchat.xyz"
#ENV BACKEND_URL="https://api.omgchat.xyz"

EXPOSE ${PORT}

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=4567", "--debug" ]
