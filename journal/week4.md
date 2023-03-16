# Week 4 — Postgres and RDS
*begin*

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
  --master-username root \
  --master-user-password Zaqswe123 \
  --allocated-storage 20 \
  --availability-zone eu-central-1a \
  --backup-retention-period 0 \
  --port 5432 \
  --no-multi-az \
  --db-name cruddur \
  --storage-type gp2 \
  --publicly-accessible \
  --storage-encrypted \
  --enable-performance-insights \
  --performance-insights-retention-period 7 \
  --no-deletion-protection
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

* Run command in CLI

```sql
psql cruddur < db/schema.sql -h localhost -U postgres
```


