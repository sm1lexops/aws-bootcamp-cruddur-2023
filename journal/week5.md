# Week 5 — DynamoDB and Serverless Caching
*begin*

## Data Modelling a Direct Messaging System using Single Table Design
*create data manipulation pattern for our application*

## Implementing DynamoDB query using Single Table Design

* Update `requirements.txt` add boto3

```sh
boto3
```

* Organaize files workspace

> Create `./backend-flask/bin/db, ../../rds directory and move db scripts to db

> Move `update-sg-rule` ../rds

> Create dir for DynamoDB ../ddb

* Create `schema-load`, `seed`, `drop` for creating table and mock data

> Create `schema-load` [DOCS for boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html)

```py
#!/usr/bin/env python3

import boto3
import sys

attrs = {
  'endpoint_urt': 'http://localhost:800'
}
if len(sys.argv) == 2;
  if "prod" in sys.argv[1]:
    attrs = {}
ddb = boto3.client('dynamodb', **attrs)

table_name = 'cruddur-message'

response = ddb.create_table(
  TableName=table_name,
  AttributeDefinitions=[
    {
      'AttributeName': 'pk',
      'AttributeType': 'S'
    },
    {
      'AttributeName': 'sk',
      'AttributeType': 'S'
    },
  ],
  KeySchema=[
    {
      'AttributeName': 'pk',
      'KeyType': 'HASH'
    },
    {
      'AttributeName': 'sk',
      'KeyType': 'RANGE'
    },
  ],
  #GlobalSecondaryIndexes=[
  #],
  BillingMode='PROVISIONED',
  ProvisionedThroughput={
      'ReadCapacityUnits': 5,
      'WriteCapacityUnits': 5
  }
)

print(response)
```

* Change permission `chmod x+u ./schema-load`, UP docker compose and try run script

> You should get json answer in cli
