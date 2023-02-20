# Week 0 — Billing and Architecture

## Homework Tasks

### Install AWS CLI

- Tutorial for installing AWS CLI [AWS CLI Install Instructions]https://docs.aws.amazon.com/cli/latest/userguide/getting-started-version.html

### Install AWS CLI for our SDE Gitpod

```sh
gp init # for initialize our .gitpod.yml conf file
```
### Add next instructions to .gitpod.yml file

    ```sh
tasks:
  - name: aws-cli
    env:
      AWS_CLI_AUTO_PROMPT: on-partial
    init: |
      cd /workspace
      curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
      unzip awscliv2.zip
      sudo ./aws/install
      cd $THEIA_WORKSPACE_ROOT
```