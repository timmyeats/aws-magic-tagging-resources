# aws-magic-tagging-resources

Use the EventBridge to trigger a Lambda function to tag resources in AWS.

## Prerequisites

- Install terraform

- Install AWS CLI

- Set AWS credential in your environment, ```aws configure  --profile your_profile_name```

- Set AWS profile in your environment, ```export AWS_PROFILE=your_profile_name```

## Configuration

Modify ```terraform.tfvars.template``` to ```terraform.tfvars```, and set the tfvars

- resource_tags = {
  terraform = "true"
  project   = "aws-magic-tagging-resources"
  version   = "v1.0.0"
}

## Deploy & Delete resources

- Deploy resources:

   `terraform init`

   `terraform plan`

   `terraform apply`

- Delete resources:

   `terraform destroy`

## Resources

- Lambda Function
- IAM Role
- IAM Policy
- Log Group
- EventBridge Rule

## How to use this

Deploy this terraform and verify the resource tags are created.

```
Default tags:

-  Owner
-  SourceIP
-  UserType
-  EventTime
-  UserName / RoleName

```
