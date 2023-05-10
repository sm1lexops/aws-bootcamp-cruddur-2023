# Week 9 — CI/CD with CodePipeline, CodeBuild and CodeDeploy

This week we'll study how to authomate our continuous integration and continuous delivery/continuous deployment chain.

- [Preparation](#preparation)
- [AWS CodeBuild](#aws-codebuild)
- [AWS CodePipeline](#aws-codepipeline)
- [Test Pipeline](#test-pipeline)

## Preparation

Create the following two scripts:

- `backend-flask/buildspec.yml`, change the env variables to your owns ([code]())
- `aws/policies/ecr-codebuild-backend-role.json` ([code]())