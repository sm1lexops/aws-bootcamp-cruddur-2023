# Week 8 — Serverless Image Processing

This week we need to use CDK (Cloud Development Kit) to create S3 buckets, Lambda functions, SNS topics, etc., allowing users to upload their avatars to update their profiles.

- [Serverless Image Processing](#serverless-image-processing)
- [Preparation](#preparation)
- [Implement CDK Stack](#implement-cdk-stack)
- [Serving Avatars via CloudFront](#serving-avatars-via-cloudfront)
- [Backend and Frontend for Profile Page](#backend-and-frontend-for-profile-page)
- [DB Migration](#db-migration)
- [Implement Avatar Uploading](#implement-avatar-uploading)
- [Double Check Environment Variables](#double-check-environment-variables)
- [Proof of Implementation](#proof-of-implementation)


## Preparation

There are some commands to run every time before and after docker compose up. To be done more efficiently, create the following scripts as seen in `./bin/start-dev-env`

> Add to `.gitpod.yml`

```sh
cd ../thumbing-serverless-cdk
npm install aws-cdk -g
cp .env.cdk .env
npm i
cd ../
```

## Implement CDK Stack

Firstly, manually create a S3 bucket named `assets.<domain_name>` (e.g., `assets.omgchat.xyz`), which will be used for serving processed images in the profile page. Then create a folder named `banners`, and upload a `banner.jpg` in there.

Secondly, export following env vars according to your domain name and another S3 bucket (e.g., `omgchat-uploaded-avatars`), which will be created by CDK later for saving the original uploaded avatar images:

```sh
export DOMAIN_NAME=omgchat.xyz
gp env DOMAIN_NAME=omgchat.xyz
export UPLOADS_BUCKET_NAME=omgchat-uploaded-avatars
gp env UPLOADS_BUCKET_NAME=omgchat-uploaded-avatars
```

In order to process uploaded images to a specific dimension, a Lambda function will be created by CDK. This function and related packages are specified in the scripts created by the following in ([repo](https://github.com/sm1lexops/aws-bootcamp-cruddur-2023/tree/week-8/aws/lambdas/process-images)):

```sh
mkdir -p aws/lambdas/process-images
cd aws/lambdas/process-images
touch index.js s3-image-processing.js test.js  example.json
npm init -y
npm install sharp @aws-sdk/client-s3
```

To check if the created Lambda function works or not, create scripts by the following commands in ([repo](https://github.com/sm1lexops/aws-bootcamp-cruddur-2023/tree/week-8/bin/avatar)) and upload a profile picture named `data.jpg` inside the created folder `files`:

```sh
cd /workspace/aws-bootcamp-cruddur-2023
mkdir -p bin/avatar
cd bin/avatar
touch build upload clear
chmod u+x build upload clear
mkdir files
```

> Download avatar image into `./bin/avatar/files` directory

Now we can initialize CDK and install related packages:

```sh
cd /workspace/aws-bootcamp-cruddur-2023
mkdir thumbing-serverless-cdk
cd thumbing-serverless-cdk
npm install aws-cdk -g
cdk init app --language typescript
npm install dotenv
```

> Create ENV VAR file `./thumbling-serverless-cdk/.env.cdk` 

Update `.env.cdk` ([reference code](https://github.com/beiciliang/aws-bootcamp-cruddur-2023/blob/week-8/thumbing-serverless-cdk/.env.example)), and run `cp .env.cdk .env`. Update [./bin/thumbing-serverless-cdk.ts](https://github.com/sm1lexops/aws-bootcamp-cruddur-2023/blob/week-8/thumbing-serverless-cdk/bin/thumbing-serverless-cdk.ts) and [./lib/thumbing-serverless-cdk-stack.ts](https://github.com/sm1lexops/aws-bootcamp-cruddur-2023/blob/week-8/thumbing-serverless-cdk/lib/thumbing-serverless-cdk-stack.ts).

In order to let the `sharp` dependency work in Lambda, run the script:

```sh
cd /workspace/aws-bootcamp-cruddur-2023
./bin/avatar/build

cd thumbing-serverless-cdk
```

> Now run 

```sh
cdk synth
```

> You can debug and observe the generated `cdk.out`

> Run 

```sh
cdk bootstrap "aws://${AWS_ACCOUNT_ID}/${AWS_DEFAULT_REGION}"
```

> Finally run 

```sh
cdk deploy
```

You can observe your what have been created on AWS CloudFormation stack of `ThumbingServerlessCdkStack`.


After running `./bin/avatar/upload`, at AWS we can see there is `data.jpg` uploaded into the `omgchat-uploaded-avatars` S3 bucket, which triggers `ThumbLambda` function to process the image, and then saves the processed image into the `avatars` folder in the `assets.omgchat.xyz` S3 bucket.

## Serving Avatars via CloudFront

Amazon CloudFront is designed to work seamlessly with S3 to serve your S3 content in a faster way. Also, using CloudFront to serve s3 content gives you a lot more flexibility and control. To create a CloudFront distribution, a certificate in the `eu-central-1` zone for `*.<your_domain_name>` is required. If you don't have one yet, create one via AWS Certificate Manager, and click "Create records in Route 53" after the certificate is issued.

Create a distribution by:

- set the Origin domain to point to `assets.<your_domain_name>`
- choose Origin access control settings (recommended) and create a control setting
- select Redirect HTTP to HTTPS for the viewer protocol policy
- choose CachingOptimized, CORS-CustomOrigin as the optional Origin request policy, and SimpleCORS as the response headers policy
- set Alternate domain name (CNAME) as `assets.<your_domain_name>`
- choose the previously created ACM for the Custom SSL certificate.

Remember to copy the created policy to the `assets.<your_domain_name>` bucket by editing its bucket policy.

In order to visit https://assets.<your_domain_name>/avatars/data.jpg to see the processed image, we need to create a record via Route 53:

- set record name as `assets.<your_domain_name>`
- turn on alias, route traffic to alias to CloudFront distribution

In my case, you can see my profile at https://assets.omgchat.xyz/avatars/data.jpg.

## Backend and Frontend for Profile Page

> For the backend, update/create the following scripts in ([db/sql repo](https://github.com/sm1lexops/aws-bootcamp-cruddur-2023/tree/week-8/backend-flask/db/sql/users)):

- `backend-flask/db/sql/users/show.sql` to get info about user
- `backend-flask/db/sql/users/update.sql` to update bio

> [services repo](https://github.com/sm1lexops/aws-bootcamp-cruddur-2023/tree/week-8/backend-flask/services)
- `backend-flask/services/user_activities.py`
- `backend-flask/services/update_profile.py`
- `backend-flask/app.py`

For the frontend, update/create the following scripts ([frontend repo](https://github.com/beiciliang/aws-bootcamp-cruddur-2023/tree/week-8/frontend-react-js)):

- `frontend-react-js/src/components/ActivityFeed.js`
- `frontend-react-js/src/components/CrudButton.js`
- `frontend-react-js/src/components/DesktopNavigation.js` to change the hardcoded url into yours
- `frontend-react-js/src/components/EditProfileButton.css`
- `frontend-react-js/src/components/EditProfileButton.js`
- `frontend-react-js/src/components/Popup.css`
- `frontend-react-js/src/components/ProfileAvatar.css`
- `frontend-react-js/src/components/ProfileAvatar.js`
- `frontend-react-js/src/components/ProfileForm.css`
- `frontend-react-js/src/components/ProfileForm.js` to let user edit their profile page
- `frontend-react-js/src/components/ProfileHeading.css`
- `frontend-react-js/src/components/ProfileHeading.js` to display profile details
- `frontend-react-js/src/components/ProfileInfo.js`
- `frontend-react-js/src/components/ReplyForm.css`
- `frontend-react-js/src/pages/HomeFeedPage.js`
- `frontend-react-js/src/pages/NotificationsFeedPage.js`
- `frontend-react-js/src/pages/UserFeedPage.js` to fetch data
- `frontend-react-js/src/lib/CheckAuth.js`
- `frontend-react-js/src/App.js`
- `frontend-react-js/jsconfig.json`

## DB Migration

Since our previous postgres database didn't have the column for saving bio, migration is required. We also need to update some backend scripts in order to let users edit bio and save the updated bio in the database.

* Create an empty `backend-flask/db/migrations/.keep`, and an executable script [`bin/generate/migration` - code](https://github.com/sm1lexops/aws-bootcamp-cruddur-2023/blob/week-8/bin/db/migrate). 

* Run `./bin/generate/migration add_bio_column`, a python script such as `backend-flask/db/migrations/1683116766_add_bio_column.py` will be generated. Edit the generated python script with SQL commands as seen in [code](https://github.com/sm1lexops/aws-bootcamp-cruddur-2023/blob/week-8/backend-flask/db/migrations/1683116766_add_bio_column.py).

* Update [`backend-flask/db/schema.sql` - code](https://github.com/sm1lexops/aws-bootcamp-cruddur-2023/blob/week-8/backend-flask/db/schema.sql), and update [`backend-flask/lib/db.py`](https://github.com/sm1lexops/aws-bootcamp-cruddur-2023/blob/week-8/backend-flask/lib/db.py) with verbose option.

* Create executable scripts [`bin/db/migrate`](https://github.com/sm1lexops/aws-bootcamp-cruddur-2023/blob/week-8/bin/db/migrate) and [`bin/db/rollback`](https://github.com/sm1lexops/aws-bootcamp-cruddur-2023/blob/week-8/bin/db/rollback). 

> First time you need connect to `psql` and run

```sql
CREATE TABLE IF NOT EXISTS public.schema_information (
  id integer UNIQUE,
  last_successful_run text
);

INSERT INTO public.schema_information (id, last_successful_run)
VALUES(1, '0')
ON CONFLICT (id) DO NOTHING;
INSERT 0 1
```

> Then run `./bin/db/migrate`, a new column called bio will be created in the db table of `users`.

> You can rollback changes with `./bin/db/rollback`
## Implement Avatar Uploading

Firstly we need to create an API endpoint, which invoke a presigned URL like `https://<API_ID>.execute-api.<AWS_REGION>.amazonaws.com`. This presigned URL can give access to the S3 bucket (`beici-cruddur-uploaded-avatars` in my case), and can deliver the uploaded image to the bucket.

We will call `https://<API_ID>.execute-api.<AWS_REGION>.amazonaws.com/avatars/key_upload` to do the upload, where the `/avatars/key_upload` resource is manipulated by the `POST` method. We will also create a Lambda function named `CruddurAvatarUpload` to decode the URL and the request. In addition, we need to implement authorization with another Lambda function named `CruddurApiGatewayLambdaAuthorizer`, which is important to control the data that is allowed to be transmitted from our gitpod workspace using the APIs.

To successfully implement above setups:

- in `aws/lambdas/cruddur-upload-avatar/`, create a basic `function.rb` and run `bundle init`; edit the generated `Gemfile`, then run `bundle install` and `bundle exec ruby function.rb`; a presigned url can be generated for local testing. The actual `function.rb` used in `CruddurAvatarUpload` is shown as in [this code](https://github.com/beiciliang/aws-bootcamp-cruddur-2023/blob/week-8/aws/lambdas/cruddur-upload-avatar/function.rb).
- in `aws/lambdas/lambda-authorizer/`, create `index.js`, run `npm install aws-jwt-verify --save`, and download everything in this folder into a zip file (you can zip by command `zip -r lambda_authorizer.zip .`), which will be uploaded into `CruddurApiGatewayLambdaAuthorizer`.

At AWS Lambda, create the corresponding two functions:

1. `CruddurAvatarUpload`

   - code source as seen in `aws/lambdas/cruddur-upload-avatar/function.rb` with your own gitpod frontend URL as `Access-Control-Allow-Origin`
   - Create ruby lambda layer, for that:

   > Create [script for adding ruby jwt lambda layer](https://github.com/sm1lexops/aws-bootcamp-cruddur-2023/blob/week-8/bin/lambda-layers/ruby-jwt)

   > Add this layer to your Lambda  `CruddurAvatarUpload` function

   - At the Lambda `Code` tab rename Handler as *function.handler* in the `Runtime settings`
   - add environment variable `UPLOADS_BUCKET_NAME`
   - create a new policy `PresignedUrlAvatarPolicy` as seen in `aws/policies/s3-upload-avatar-presigned-url-policy.json` ([code](https://github.com/beiciliang/aws-bootcamp-cruddur-2023/blob/week-8/aws/policies/s3-upload-avatar-presigned-url-policy.json)), and then attach this policy to the role of this Lambda

2. `CruddurApiGatewayLambdaAuthorizer`

   - upload `lambda_authorizer.zip` into the code source
   - add environment variables `USER_POOL_ID` and `CLIENT_ID`

*Repit with strong knowledge and debugging skills* - Different from Andrew's video and his codes, I don't have a layer of JWT cause I passed the JWT sub from `CruddurApiGatewayLambdaAuthorizer` to `CruddurAvatarUpload` ([reference](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-lambda-authorizer.html)).

At AWS S3, update the permissions of `omgchat-uploaded-avatars` by editing the CORS configuration as seen in `aws/s3/cors.json` ([code](https://github.com/beiciliang/aws-bootcamp-cruddur-2023/blob/week-8/aws/s3/cors.json)).

At AWS API Gateway, create `api.<domain_name>` (in my case `api.omgchat.xyz`), create two routes:

- `POST /avatars/key_upload` with integration `CruddurAvatarUpload`
- `POST /avatars/key_upload` create authorizer `CruddurJWTAuthorizer` which invoke Lambda `CruddurApiGatewayLambdaAuthorizer`
- `OPTIONS /{proxy+}` without authorizer, but with integration `CruddurAvatarUpload`


Noted that we don't need to configure CORS at API Gateway. If you did before, click "Clear" to avoid potential CORS issues.

## Double Check Environment Variables

There are some environment variables and setups worth double checking:

- `function.rb` in `CruddurAvatarUpload`: set `Access-Control-Allow-Origin` as your own frontend URL.
- `index.js` in `CruddurApiGatewayLambdaAuthorizer`: make sure that token can be correctly extracted from the authorization header.
- Environment variables in the above two Lambdas were added.
- `erb/frontend-react-js.env.erb`: `REACT_APP_API_GATEWAY_ENDPOINT_URL` equals to the Invoke URL shown in the API Gateway.
- `frontend-react-js/src/components/ProfileForm.js`: `gateway_url` and `backend_url` are correctly set.
- Pay attention to variable name inconsistency in some scripts, e.g., `cognito_user_uuid` vs. `cognito_user_id`.

## Proof of Implementation

