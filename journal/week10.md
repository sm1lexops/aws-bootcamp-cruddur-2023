# Week 10 — CloudFormation Part 1

*This week we'll study how to use CloudFormation for our Project.*

*Be patient during **Hardest** but very **Exciting** week-10*

- [Preparation](#preparation)

- [Network CloudFormation Template](#network-cloudformation-template)

- [Cluster CloudFormation Template](#cluster-cloudformation-template)

- [AWS RDS Postgresql CloudFormation Template](#aws-rds-postgresql-cloudformation-template)

- [Services CloudFormation Template](#services-cloudformation-template)

- [Frontend CloudFormation Template](#frontend-cloudformation-template)

- [CICD CloudFormation Template](#cicd-cloudformation-template)

- [Summary](#summary)

## Preparation

> Full template example [AWS CloudFormation Template ECS snippets](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/quickref-ecs.html#quickref-ecs-example-1.yaml)

* First of all you can delete all resources, all your `HARD WORK`, but I don't advice doing that, the best choice is to create new `namespace` and change name for all services and resources.

* In my case, I was deleting all resources and should change `Route 53` record for new `ALB`. In that case you'll have new VPC, SecGroup and some other kind of stuff for troubleshooting.

## Network CloudFormation Template

> In all cases for sending ENV VAR to cfn `template.yaml`  we using `parameters.json` file




## Cluster CloudFormation Template




## AWS RDS Postgresql CloudFormation Template




## Services CloudFormation Template





## Frontend CloudFormation Template

> Frontend

* Need certificate `arn` from `us-east-1`, because CloudFront services using global cert






## CICD CloudFormation Template

> CICD Planning

* Create CloudFormation Template

* Create cicd-deploy script, tmp dir for output package

* Create artifact bucket

* Authorize to Github, update pending connections for pipeline

* Update branch, merge `week-10` to `prod` branch 

## Summary


