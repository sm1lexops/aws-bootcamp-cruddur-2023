# Week X — Cleanup

- [Preparation](#preparation)

- [Reconnect Database and Post Confirmation Lambda](#reconnect-database-and-post-confirmation-lambda)

- [Refactoring Ddb](#refactoring-ddb)

- [Refactoring and CleanUp](#refactoring-and-cleanup)

- [Summary](#summary)

## Preparation

* Create [`static-build-frontend`](https://github.com/sm1lexops/aws-bootcamp-cruddur-2023/blob/week-10/bin/frontend/static-build-frontend) script for deploying static web resources

* Run `static-build-frontend` script and Fix main frontend issues [fix#1](https://github.com/sm1lexops/aws-bootcamp-cruddur-2023/commit/bc8cf83cc722dbe3fa8f004bfa5af07fa9b0fe7a) and [fix#2](https://github.com/sm1lexops/aws-bootcamp-cruddur-2023/commit/eee5ff7f55610946c47fb695533fbc022f037bf3)

* Zip all static frontend content to deliver to S3 

* Create or install Gemfile for `aws_s3_website_sync` and `dotenv`

* Create rake file for sync and run sync

* Before run sync script don't forget run `npm install` and `npm build` in frontend dir

> Rake file for sync [`sync-static-s3`](https://github.com/sm1lexops/aws-bootcamp-cruddur-2023/blob/week-x/bin/frontend/sync-static-s3) file:

```ruby
#!/usr/bin/env ruby
puts("==== Installing <gem install aws_s3_website_sync> ====")
require 'bundler/inline'
require 'nokogiri'

gemfile do
  source 'https://rubygems.org'
  gem 'aws_s3_website_sync', require: true
  gem 'dotenv', require: true 
end

require 'aws_s3_website_sync'
require 'dotenv'

env_path = "/workspace/aws-bootcamp-cruddur-2023/erb/sync.env"
Dotenv.load(env_path)

puts "== configuration"
puts "aws_default_region:   #{ENV["AWS_DEFAULT_REGION"]}"
puts "s3_bucket:            #{ENV["SYNC_S3_BUCKET"]}"
puts "distribution_id:      #{ENV["SYNC_CLOUDFRONT_DISTRUBTION_ID"]}"
puts "build_dir:            #{ENV["SYNC_BUILD_DIR"]}"

changeset_path = ENV["SYNC_OUTPUT_CHANGESET_PATH"]
changeset_path = changeset_path.sub(".json","-#{Time.now.to_i}.json")

puts "output_changset_path: #{changeset_path}"
puts "auto_approve:         #{ENV["SYNC_AUTO_APPROVE"]}"

puts("==== Syncing static content with AWS S3 Bucket ====")

puts "sync =="
AwsS3WebsiteSync::Runner.run(
  aws_access_key_id:     ENV["AWS_ACCESS_KEY_ID"],
  aws_secret_access_key: ENV["AWS_SECRET_ACCESS_KEY"],
  aws_default_region:    ENV["AWS_DEFAULT_REGION"],
  s3_bucket:             ENV["SYNC_S3_BUCKET"],
  distribution_id:       ENV["SYNC_CLOUDFRONT_DISTRUBTION_ID"],
  build_dir:             ENV["SYNC_BUILD_DIR"],
  output_changset_path:  changeset_path,
  auto_approve:          ENV["SYNC_AUTO_APPROVE"],
  silent: "ignore,no_change",
  ignore_files: [
    'stylesheets/index',
    'android-chrome-192x192.png',
    'android-chrome-256x256.png',
    'apple-touch-icon-precomposed.png',
    'apple-touch-icon.png',
    'site.webmanifest',
    'error.html',
    'favicon-16x16.png',
    'favicon-32x32.png',
    'favicon.ico',
    'robots.txt',
    'safari-pinned-tab.svg'
  ]
)
```

> You should get All info about changes at your static content and invalidation 

```sh
I, [2023-07-02T17:18:58.148418 #9677]  INFO -- : Runner.run
I, [2023-07-02T17:18:58.148484 #9677]  INFO -- : List.local
I, [2023-07-02T17:18:58.166242 #9677]  INFO -- : List.remote
I, [2023-07-02T17:18:58.317970 #9677]  INFO -- : Plan.delete
I, [2023-07-02T17:18:58.318070 #9677]  INFO -- : Plan.create_update
---[ Plan ]------------------------------------------------------------
ChangeSet: changeset-1688318338

WebSync will perform the following operations:

        update asset-manifest.json
        update index.html
        create static/js/main.a5e24caa.js
        create static/js/main.a5e24caa.js.LICENSE.txt
        create static/js/main.a5e24caa.js.map
        delete static/js/main.b3a8eed0.js
        delete static/js/main.b3a8eed0.js.LICENSE.txt
        delete static/js/main.b3a8eed0.js.map
--------------------------------------------------------------------
ignore: 8   delete: 3   create: 3   update: 2   no_change: 23
...

Invalidation IF5LMAJ31WAWUV8YPWZDRP28R8 has been created. Please wait about 60 seconds for it to finish.
```

![Invalidation](assets/week-x/cf_invalidation.jpg)


## Reconnect Database and Post Confirmation Lambda

*the main issues was in Lambda Post Confirmation function:*

* First [Check code](https://github.com/sm1lexops/aws-bootcamp-cruddur-2023/blob/week-x/aws/lambdas/cruddur-post-confirrmation.py)

* Next check `CONNECTION_URL` and update it

* After run `schema-load`, `migrate` and `seed` scripts for Loading data into rds

* Delete your old user from `Cognito` and join one more time to `omgchat.xyz`

* Check your connection to `prod` postresql, before that you'll need update `GITPOD_IP`, `DB_SG_ID` and `DB_SG_RULE_ID` and run [`update-sg-rule`](https://github.com/sm1lexops/aws-bootcamp-cruddur-2023/blob/week-x/bin/rds/update-sg-rule) to give access to RDS

> You should have access

```sh
psql $CONNECTION_URL_PROD
```

* Check your new user from Database and run command bellow

> You should see something like that, <cognito_user_id> shouldn't be empty

```sh
omgchat=> select * from users;
                 uuid                 |  display_name   | handle  |          email           |           cognito_user_id            |         created_at         
--------------------------------------+-----------------+---------+--------------------------+--------------------------------------+----------------------------
 7fd6217e-8515-4275-8d9e-957d700587dc | Aleksey Smirnov | smirnov | smilovesmirnov@gmail.com | 9bf48207-9665-4f2d-8f1d-40da7007aa92 | 2023-07-03 16:15:04.243368
(4 rows)

omgchat=> 
```

* Check that you can take a `Crud`, resolve issues

## Refactoring Ddb

* Add ENV VAR `DDB_MESSAGE_TABLE="OmgDdb-DynamoDBTable-KWLL3BZ0AUVY"` into `backend-flask.env`

* Change table name `ddb.py` 4 line

```sh
table_name = os.getenv("DDB_MESSAGE_TABLE")
```

* Add ENV VAR to the `template.yaml`

```yaml
            - Name: 'DDB_MESSAGE_TABLE'
              Value: !Ref DDBMessageTable
```

* Create AWS CFN for MachineUser DynamoDB

> [`template.yaml`](https://github.com/sm1lexops/aws-bootcamp-cruddur-2023/blob/week-x/aws/cfn/machine-user/template.yaml)

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  OmgchatMachineUser:
    Type: 'AWS::IAM::User'
    Properties: 
      UserName: 'omgchat_machine_user'
  DynamoDBFullAccessPolicy: 
    Type: 'AWS::IAM::Policy'
    Properties: 
      PolicyName: 'DynamoDBFullAccessPolicy'
      PolicyDocument:
        Version: '2012-10-17'
        Statement: 
          - Effect: Allow
            Action: 
              - dynamodb:PutItem
              - dynamodb:GetItem
              - dynamodb:Scan
              - dynamodb:Query
              - dynamodb:UpdateItem
              - dynamodb:DeleteItem
              - dynamodb:BatchWriteItem
            Resource: '*'
      Users:
        - !Ref OmgchatMachineUser
```

* Create and run script

> [`machine-user-deployq](https://github.com/sm1lexops/aws-bootcamp-cruddur-2023/blob/week-x/bin/cfn/machine-user-deploy)

```sh
#! /usr/bin/env bash 
set -e
CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="=====  MachineUser for DDB CloudFormation deploy ====="
printf "${CYAN}==== ${LABEL}${NO_COLOR} ${CYAN}======${NO_COLOR}\n"
CFN_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/cfn/machine-user/template.yaml"
REGION="eu-central-1"
STACK_NAME="OmgMachineUser"
BUCKET="omg-cfn-artifact"

aws cloudformation deploy \
  --stack-name $STACK_NAME \
  --s3-bucket $BUCKET \
  --s3-prefix db \
  --region $REGION \
  --template-file $CFN_PATH \
  --no-execute-changeset \
  --tags group=omgchat-machine-user \
  --capabilities CAPABILITY_NAMED_IAM
```

## Refactoring and CleanUp

* Refactoring routes -> [commit](https://github.com/sm1lexops/aws-bootcamp-cruddur-2023/commit/6e63bdbdfce4d8a6d73d243f30dd91491f04586d)

* Add Initialization apps -> [commit](https://github.com/sm1lexops/aws-bootcamp-cruddur-2023/commit/b2c638e831b3a8e38a3888500380fbf1c602a7c8)

* Update activities and notification form > [commit-1](https://github.com/sm1lexops/aws-bootcamp-cruddur-2023/commit/b2c638e831b3a8e38a3888500380fbf1c602a7c8), [commit-2](https://github.com/sm1lexops/aws-bootcamp-cruddur-2023/commit/f24bb6f0c6beef6fa69a1f5e3067a21281fd9175), [commit-3](https://github.com/sm1lexops/aws-bootcamp-cruddur-2023/commit/99413e97960024113b1db3bddc1b190e98584a62), [commit-4](https://github.com/sm1lexops/aws-bootcamp-cruddur-2023/commit/226134a532ab1a66f81bd3b24e5487ea8beee761) 

* Configure migration, change [`migration`](https://github.com/sm1lexops/aws-bootcamp-cruddur-2023/blob/week-x/bin/generate/migration) and run [db migrate script](https://github.com/sm1lexops/aws-bootcamp-cruddur-2023/blob/week-x/bin/db/migrate) 

* Fix DateTime -> [commit](https://github.com/sm1lexops/aws-bootcamp-cruddur-2023/commit/c294b43bca18890d3a6924fa2784587e8d019111)

* Refactory error handling and fetch request, update frontend -> [commit](https://github.com/sm1lexops/aws-bootcamp-cruddur-2023/commit/b1c09785755c77cda8eb645cf7da3de57d35c013)

*Well done, I'm done*

