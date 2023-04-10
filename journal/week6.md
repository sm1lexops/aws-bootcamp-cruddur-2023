# Week 6 — Deploying Containers

*begin*

## Test RDS Connecetion

* Create file for testing cluster connections

```py
#!/usr/bin/env python3

import urllib.request

try:
  response = urllib.request.urlopen('http://localhost:4567/api/health-check')
  if response.getcode() == 200:
    print("[OK] Flask server is running")
    exit(0) # success
  else:
    print("[BAD] Flask server is not running")
    exit(1) # false
# This for some reason is not capturing the error....
#except ConnectionRefusedError as e:
# so we'll just catch on all even though this is a bad practice
except Exception as e:
  print(e)
  exit(1) # false
```

> `chmod u+x ./bin/health-check` run `./bin/health-check` and you should get

```sh
<urlopen error [Errno 111] Connection refused>
```
## Create CloudWatch Log Group

```sh
aws logs create-log-group --log-group-name /cruddur/fargate-cluster
aws logs put-retention-policy --log-group-name /cruddur/fargate-cluster --retention-in-days 1
```

## Create ECS Cluster

```sh
aws ecs create-cluster \
--cluster-name cruddur \
--service-connect-defaults namespace=cruddur
```

> You should get json answer

## Create ECR repo and push image

* Create ECR repo

```sh
aws ecr create-repository \
  --repository-name cruddur-python \
  --image-tag-mutability MUTABLE
```

> Should get success json answer


## Push your first container

* 1. Retrieve an authentication token and authenticate your Docker client to your registry.
Use the AWS CLI:

```sh
aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com"
```

> Set URL for ECR 

```sh
export ECR_PYTHON_URL="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/cruddur-python"
echo $ECR_PYTHON_URL
```

* 2. Pull your Docker image using the following command. For information on building a Docker file from scratch see the instructions here . You can skip this step if your image is already built:

```sh
docker pull python:3.10-slim-buster
```

* 3. After the pull completes, tag your image so you can push the image to this repository:

```sh
docker tag python:3.10-slim-buster $ECR_PYTHON_URL:3.10-slim-buster
```

* 4. Run the following command to push this image to your newly created AWS repository:

```sh
docker push $ECR_PYTHON_URL:3.10-slim-buster
```
    
> You should get your image at ECR 

![AWS ECR repo Image](assets/week-6/ecr_image.jpg)


