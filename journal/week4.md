# Week 4 — Postgres and RDS
*begin*

## Common PSQL Commands

```sql
\x on -- expanded display when looking at data
\q -- Quit PSQL
\l -- List all databases
\c database_name -- Connect to a specific database
\dt -- List all tables in the current database
\d table_name -- Describe a specific table
\du -- List all users and their roles
\dn -- List all schemas in the current database
CREATE DATABASE database_name; -- Create a new database
DROP DATABASE database_name; -- Delete a database
CREATE TABLE table_name (column1 datatype1, column2 datatype2, ...); -- Create a new table
DROP TABLE table_name; -- Delete a table
SELECT column1, column2, ... FROM table_name WHERE condition; -- Select data from a table
INSERT INTO table_name (column1, column2, ...) VALUES (value1, value2, ...); -- Insert data into a table
UPDATE table_name SET column1 = value1, column2 = value2, ... WHERE condition; -- Update data in a table
DELETE FROM table_name WHERE condition; -- Delete data from a table
```

## Check your dev environment

* First need uncoment line for postgesql db

* Up docker compose and set visible port `5432`

* Check your connections 

```sh
psql -U postgres -h localhost
```

> *postgres=#*`\du` 

You should see 

```sh
                                   List of roles
 Role name |                         Attributes                         | Member of 
-----------+------------------------------------------------------------+-----------
 postgres  | Superuser, Create role, Create DB, Replication, Bypass RLS | {}
 ```

* Check your AWS connections 

```sh
aws sts get-caller-identity
```

## Create AWS RDS postgresql DB instance

> Input to CLI

```sh
aws rds create-db-instance \
  --db-instance-identifier cruddur-db-instance \
  --db-instance-class db.t4g.micro \
  --engine postgres \
  --engine-version  14.6 \
  --master-username psqlroot \
  --master-user-password Zaqswe_123 \
  --allocated-storage 20 \
  --availability-zone eu-central-1a \
  --backup-retention-period 0 \
  --port 5432 \
  --no-multi-az \
  --db-name cruddur \
  --storage-type gp2 \
  --publicly-accessible \
  --storage-encrypted \
  --no-deletion-protection

  # optional
  --enable-performance-insights \
  --performance-insights-retention-period 7 \
  ```

* You should get json answer

```js
{
    "DBInstance": {
        "DBInstanceIdentifier": "cruddur-db-instance",
        "DBInstanceClass": "db.t4g.micro",
        "Engine": "postgres",
        "DBInstanceStatus": "creating",
        "MasterUsername": "root",
        "DBName": "cruddur",
        "AllocatedStorage": 20,
        "PreferredBackupWindow": "20:13-20:43",
        "BackupRetentionPeriod": 0,
        "DBSecurityGroups": [],
        "VpcSecurityGroups": [
            {
                "VpcSecurityGroupId": "sg-0075ce6b8a9248567",
                "Status": "active"
```

After 10-15 minutes check your AWS RDS Instance

![RDS Instance](assets/week-4/rds_instance.jpg)

* Create `./backend-flask/db/schema.sql` file to import cruddur db

> Add to schema.sql to have postgres generate out `uuid`

```sh
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

> Create tables `public.users` and `public.activities`

```sql
DROP TABLE IF EXISTS public.users;
DROP TABLE IF EXISTS public.activities;

CREATE TABLE public.users (
  uuid UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  display_name text,
  handle text,
  cognito_user_id text,
  created_at TIMESTAMP default current_timestamp NOT NULL
);

CREATE TABLE public.activities (
  uuid UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_uuid UUID NOT NULL,
  message text NOT NULL,
  replies_count integer DEFAULT 0,
  reposts_count integer DEFAULT 0,
  likes_count integer DEFAULT 0,
  reply_to_activity_uuid integer,
  expires_at TIMESTAMP,
  created_at TIMESTAMP default current_timestamp NOT NULL
);
```

* Run command in CLI

```sql
psql cruddur < ./backend-flask/db/schema.sql -h localhost -U postgres
```

> Output

```sh
Password for user postgres: 
CREATE EXTENSION
```

* We can automate our connections to DB, adding SECRET to your ENV VAR 

> you can add this to secret codespace or gitpod

```sh
CONNECTION_PSQL="[user[:password]@][network_location][:port][/dbname][?param1=value1&...]
```

> rebuild SDE and then try

```sh
psql $CONNECTION_PSQL
```

## Create Scripts for DB Management 

> Create `./backend-flask/bin/db-connect`

```sh
#! /usr/bin/bash

if [ "$1" = "prod" ]; then
  echo "Running in production mode"
  URL=$CONNECTION_PSQL_PROD
else
  URL=$CONNECTION_PSQL_DEV
fi

psql $URL
```

> Create `./backend-flask/bin/db-create`

```sh
#!/usr/bin/bash 

CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="db-create"
printf "${CYAN}== ${LABEL}${NO_COLOR}\n"

NO_DB_CONNECTION_URL=$(sed "s/\/cruddur/ /g" <<< "$CONNECTION_PSQL_DEV")
psql $NO_DB_CONNECTION_URL -c "SELECT 1 FROM pg_database WHERE datname = 'cruddur'" | grep -q 1 | psql $NO_DB_CONNECTION_URL -c "CREATE DATABASE cruddur;"

echo $0
```

> Create `./backend-flask/bin/db-drop`

```sh
#!/usr/bin/bash 

CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="db-create"
printf "${CYAN}== ${LABEL}${NO_COLOR}\n"

NO_DB_CONNECTION_URL=$(sed "s/\/cruddur/ /g" <<< "$CONNECTION_PSQL_DEV")
psql $NO_DB_CONNECTION_URL -c "SELECT 1 FROM pg_database WHERE datname = 'cruddur'" | grep -q 1 | psql $NO_DB_CONNECTION_URL -c "DROP DATABASE cruddur;"

echo "====DATABASE <cruddur> DROP SUCCESS===="
echo $0
```

> Create `./backend-flask/bin/db-schema-load`

```sh
#!/usr/bin/bash -xe

CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="db-schema-load"
printf "${CYAN}== ${LABEL}${NO_COLOR}\n"

schema_path="./backend-flask/db/schema.sql"
echo $schema_path

if [ "$1" = "prod" ]; then
  echo "Running in production mode"
  URL=$CONNECTION_PSQL_PROD
else
  URL=$CONNECTION_PSQL_DEV
fi

psql $URL cruddur < $schema_path
```

> Create `./backend-flask/bin/db-seed`

```sh
#! /usr/bin/bash

#echo "== db-seed"
CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="db-seed"
printf "${CYAN}== ${LABEL}${NO_COLOR}\n"

seed_path="./backend-flask/db/seed.sql"

echo $seed_path

psql $CONNECTION_PSQL_DEV cruddur < $seed_path
```

> Create `./backend-flask/bin/db-session`

```sh
#! /usr/bin/bash
CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="db-sessions"
printf "${CYAN}== ${LABEL}${NO_COLOR}\n"

if [ "$1" = "prod" ]; then
  echo "Running in production mode"
  URL=$CONNECTION_PSQL_PROD
else
  URL=$CONNECTION_PSQL_DEV
fi

NO_DB_URL=$(sed 's/\/cruddur//g' <<<"$URL")
psql $NO_DB_URL -c "select pid as process_id, \
       usename as user,  \
       datname as db, \
       client_addr, \
       application_name as app,\
       state \
from pg_stat_activity;"
```

For convenience you can create symlink for script files

```sh
ln -sf ./backend-flask/bin/db-<your file> <symlink_name_for_your_file>
```

* Now you can use scripts > drop database `./db-drop`

```sh
== db-drop
DROP DATABASE
====DATABASE <cruddur> DROP SUCCESS====
```

* Create Database `./db-create`

```sh
== db-create
CREATE DATABASE
```

* Load Schema to Database `./db-schema-load`

```sh
CREATE EXTENSION
NOTICE:  table "users" does not exist, skipping
DROP TABLE
NOTICE:  table "activities" does not exist, skipping
DROP TABLE
CREATE TABLE
CREATE TABLE
```

* Load Seed to Schema `./db-seed`

```sh
== db-seed
./backend-flask/db/seed.sql
INSERT 0 2
INSERT 0 1
```

* View the connections we are using `./db-session`

```sh
== db-sessions
 process_id |   user   |    db    | client_addr | app  | state  
------------+----------+----------+-------------+------+--------
         52 |          |          |             |      | 
         54 | postgres |          |             |      | 
        307 | postgres | postgres | 172.18.0.1  | psql | active
         50 |          |          |             |      | 
         49 |          |          |             |      | 
         51 |          |          |             |      | 
(6 rows)
```

* For using scripts in a bundle

> Create `./db-setup`

```sh
#! /usr/bin/bash
-e # stop if it fails at any point

#echo "==== db-setup"
CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="db-setup"
printf "${CYAN}==== ${LABEL}${NO_COLOR}\n"

bin_path="./backend-flask/bin"

source "$bin_path/db-drop"
source "$bin_path/db-create"
source "$bin_path/db-schema-load"
source "$bin_path/db-seed"
```

* Check data from table `psql $CONNECTION_PSQL_DEV -c "SELECT * FROM activities;"`

```sh
-[ RECORD 1 ]----------+-------------------------------------
uuid                   | af85d6f8-dd7a-46c5-ad5d-83f2716e9570
user_uuid              | ce5d6a60-a15a-417d-a8ad-936fa38e223f
message                | This was imported as seed data!
replies_count          | 0
reposts_count          | 0
likes_count            | 0
reply_to_activity_uuid | 
expires_at             | 2023-03-29 16:45:48.889741
created_at             | 2023-03-19 16:45:48.889741
```

## Implement Postgresql Driver for Python

* Add to `reuquirements.txt`

```sh
psycopg[binary]
psycopg[pool]
```

* Automatically update timestamp column psql

```sql
DROP TRIGGER IF EXISTS trig_users_updated_at ON users;
DROP TRIGGER IF EXISTS trig_activities_updated_at ON activities;
```

```sql
DROP FUNCTION IF EXISTS func_updated_at();
CREATE FUNCTION func_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ language 'plpgsql';
```

```sql
CREATE TRIGGER trig_users_updated_at 
BEFORE UPDATE ON users 
FOR EACH ROW EXECUTE PROCEDURE func_updated_at();
CREATE TRIGGER trig_activities_updated_at 
BEFORE UPDATE ON activities 
FOR EACH ROW EXECUTE PROCEDURE func_updated_at();
```

* Add ENV VAR to backend flask

```js
  backend-flask:
    environment:
      CONNECTION_URL: "${CONNECTION_PSQL_DEV}"
```
* Temporarily change `${CONNECTION_PSQL_DEV}` to `postgresql://postgres:password@db:5432/cruddur`

> Create `./backend-flask/lib/db.py`

```py
from psycopg_pool import ConnectionPool
import os

def query_wrap_object(template):
  sql = f"""
  (SELECT COALESCE(row_to_json(object_row),'{{}}'::json) FROM (
  {template}
  ) object_row);
  """
  return sql

def query_wrap_array(template):
  sql = f"""
  (SELECT COALESCE(array_to_json(array_agg(row_to_json(array_row))),'[]'::json) FROM (
  {template}
  ) array_row);
  """
  return sql

connection_url = os.getenv("CONNECTION_URL")
pool = ConnectionPool(connection_url)

```

> Update `home_activities.py` our mock endpoint with real API call

```py
from datetime import datetime, timedelta, timezone
from opentelemetry import trace
from lib.db import pool, query_wrap_object, query_wrap_array

tracer = trace.get_tracer("home.activities")
class HomeActivities:
  def run(cognito_user_id=None):
    #logger.info("HomeActivities")
    with tracer.start_as_current_span("home-activities-data") as outer_span:
      outer_span.set_attribute("outer", True)
      span = trace.get_current_span()
      now = datetime.now(timezone.utc).astimezone()
      span.set_attribute("app.hubabuba", now.isoformat())
      sql = query_wrap_array("""
        SELECT
          activities.uuid,
          users.display_name,
          users.handle,
          activities.message,
          activities.replies_count,
          activities.reposts_count,
          activities.likes_count,
          activities.reply_to_activity_uuid,
          activities.expires_at,
          activities.created_at
        FROM public.activities
        LEFT JOIN public.users ON users.uuid = activities.user_uuid
        ORDER BY activities.created_at DESC
        """)
      print(sql)
      with pool.connection() as conn:
        with conn.cursor() as cur:
          cur.execute(sql)
          # this will return a tuple
          # the first field being the data
          json = cur.fetchone()
      with tracer.start_as_current_span("home-results-activities") as inner_span:
        inner_span.set_attribute("inner", True)
        span = trace.get_current_span()
        span.set_attribute("app.result_length", len(sql))
      return json[0]
```

> If everything is correct

* Database created, schema and seed loaded
* Created `db.py` updated `home_activities.py`

> Up docker compose, public port 3000, and you should see 

![Data from PSQL DB](assets/week-4/pg_driver_implement.jpg)

## Connect to AWS RDS DB via SDE

We need our sde ip and add it to whitelist for inbound traffic `POSTGRESQL` 

> ENV VAR with SDE IP

```sh
GITPOD_IP=$(curl ifconfig.me)
```

> Add ENV VAR for AWS CLI (*paste your sg group #*)

```sh
export DB_SG_ID="sg-0b725ebab7e25635e"
gp env DB_SG_ID="sg-0b725ebab7e25635e"
export DB_SG_RULE_ID="sgr-070061bba156cfa88"
gp env DB_SG_RULE_ID="sgr-070061bba156cfa88"
```

> Update AWS security group for access [SG Tutorial](https://docs.aws.amazon.com/cli/latest/reference/ec2/modify-security-group-rules.html#examples)

```aws
aws ec2 modify-security-group-rules \
    --group-id $DB_SG_ID \
    --security-group-rules "Description=GitPod,SecurityGroupRuleId=$DB_SG_RULE_ID,SecurityGroupRule={IpProtocol=tcp,FromPort=5432,ToPort=5432,CidrIpv4=$GITPOD_IP/32}"
```

> Create `db-update-sg-rule`

```sh
#! /usr/bin/bash

aws ec2 modify-security-group-rules \
    --group-id $DB_SG_ID \
    --security-group-rules "Description=GitPod,SecurityGroupRuleId=$DB_SG_RULE_ID,SecurityGroupRule={IpProtocol=tcp,FromPort=5432,ToPort=5432,CidrIpv4=$GITPOD_IP/32}"
```

* Test remote Access to AWS RDS where for example `$CONNECTION_PSQL_PROD=postgresql://root:huEE33z2Qvl383@cruddur-db-instance.czz1cuvepklc.ca-central-1.rds.amazonaws.com:5433/cruddur`

```sh
psql $CONNECTION_PSQL_PROD
```

You can update your ENV VAR for SDE or add this ENV VAR to secrets services like a codespace

```sh
export PROD_CONNECTION_URL="postgresql://root:huEE33z2Qvl383@cruddur-db-instance.czz1cuvepklc.ca-central-1.rds.amazonaws.com:5432/cruddur"
gp env PROD_CONNECTION_URL="postgresql://root:huEE33z2Qvl383@cruddur-db-instance.czz1cuvepklc.ca-central-1.rds.amazonaws.com:5432/cruddur"
```

## Automate your SDE building with ENV VAR 

> Add to postgres `docker-compose.yml` file

```sh
    command: |
      export GITPOD_IP=$(curl ifconfig.me)
      source "$THEIA_WORKSPACE_ROOT/backend-flask/db-update-sg-rule"
```

## Implement AWS Cognito Post Confirmation Lambda

### Create the Handler Function

* Create lambda in same vpc as rds instance Python 3.8

* Add a layer for psycopg2 with one of the below methods for development or production

> ENV variables for the lambda environment (*change for yours*)

```sh
PG_HOSTNAME='cruddur-db-instance.czz1cuvepklc.ca-central-1.rds.amazonaws.com'
PG_DATABASE='cruddur'
PG_USERNAME='root'
PG_PASSWORD='huEE33z2Qvl383'
```

You can create Lambda in AWS Console or use [CLI for AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/configuration-vpc.html)

> To create a function and connect it to a VPC using the AWS Command Line Interface (AWS CLI), you can use the create-function command with the vpc-config option. The following example creates a function with a connection to a VPC with two subnets, one security group adn ENV VAR

```sh
aws lambda create-function \
--function-name my-function \
--runtime nodejs18.x --handler <your_code_for_lambda>.py --zip-file fileb://function.zip \
--role arn:aws:iam::123456789012:role/lambda-role \
--vpc-config SubnetIds=subnet-071f712345678e7c8,subnet-07fd123456788a036,SecurityGroupIds=sg-085912345678492fb \
```

> Create Function for AWS Lambda add to `./aws/lambda/cruddur-post-confirrmation.py`

```py
import json
import psycopg2
import os

def lambda_handler(event, context):
    user = event['request']['userAttributes']
    print('userAttributes')
    print(user)

    user_display_name  = user['name']
    user_email         = user['email']
    user_handle        = user['preferred_username']
    user_cognito_id    = user['sub']
    try:
      print('entered-try')
      sql = f"""
         INSERT INTO public.users (
          display_name, 
          email,
          handle, 
          cognito_user_id
          ) 
        VALUES(%s,%s,%s,%s)
      """
      print('SQL Statement ----')
      print(sql)
      conn = psycopg2.connect(os.getenv('CONNECTION_URL'))
      cur = conn.cursor()
      params = [
        user_display_name,
        user_email,
        user_handle,
        user_cognito_id
      ]
      cur.execute(sql,*params)
      conn.commit() 

    except (Exception, psycopg2.DatabaseError) as error:
      print(error)
    finally:
      if conn is not None:
          cur.close()
          conn.close()
          print('Database connection closed.')
    return event
```

> Update ENV VAR for AWS Lambda

```sh
aws lambda update-function-configuration \
--function-name my-function \
--environment "Variables={BUCKET=my-bucket,KEY=file.txt}"
```

* Create post confirmation trigger for AWS Lambda

