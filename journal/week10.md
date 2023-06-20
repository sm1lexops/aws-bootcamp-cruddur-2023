# Week 10 — CloudFormation Part 1

This week we'll study how to use CloudFormation for our Project.

- [Preparation](#preparation)



- []Create network/cluster/db cfn
- []

> CICD cfn

* Create artifact bucket

* Authorize to Github
## Preparation

> Full template example [AWS CloudFormation Template ECS snippets](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/quickref-ecs.html#quickref-ecs-example-1.yaml)

* First of all you can delete all resources, all your `HARD WORK`, but I don't advice doing that, the best choice is to create new `namespace` for all services and resources.

* In my case, I was deleting all resources and should change `Route 53` record for new `ALB`. In that case you'll have new VPC, SecGroup and etc.