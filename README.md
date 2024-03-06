# AWS Magic Tagging Resources

Use the EventBridge to trigger a Lambda function to tag resources in AWS.

## Prerequisites

- Install Terraform

- Install AWS CLI

- Set AWS credential in your environment, ```aws configure  --profile your_profile_name```

- Set AWS profile in your environment, ```export AWS_PROFILE=your_profile_name```

## Configuration

Modify ```terraform.tfvars.template``` to ```terraform.tfvars```, and set the tfvars

```
resource_tags = {
  terraform = "true"
  project   = "aws-magic-tagging-resources"
  version   = "v1.0.0"
}
```

## Resources

- Lambda Function
- IAM Role
- IAM Policy
- Log Group
- EventBridge Rule

## How to use this

Deploy this terraform and verify the resource tags are created.

### Deploy and Destroy

#### Resources in a single region

- Deploy resources:

   `terraform init`

   `terraform plan`

   `terraform apply`

- Destroy resources:

   `terraform destroy`

#### Resources in multiple regions

- Deploy resources:

   `sh multi-region-deploy.sh`

- Destroy resources:

   `sh multi-region-destroy.sh`


### Support auto-tagging resources

  - EC2
  - ELB
  - RDS
  - CloudFront
  - Lambda
  - SNS
  - IAM


### Default tags

  -  Owner
  -  SourceIP
  -  UserType
  -  EventTime
  -  UserName / RoleName


<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 0.14 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | 4.22.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | 4.22.0 |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_lambda"></a> [lambda](#module\_lambda) | terraform-aws-modules/lambda/aws | 3.3.1 |

## Resources

| Name | Type |
|------|------|
| [aws_cloudwatch_dashboard.dashboard](https://registry.terraform.io/providers/hashicorp/aws/4.22.0/docs/resources/cloudwatch_dashboard) | resource |
| [aws_cloudwatch_event_rule.event_rule](https://registry.terraform.io/providers/hashicorp/aws/4.22.0/docs/resources/cloudwatch_event_rule) | resource |
| [aws_cloudwatch_event_target.event_rule](https://registry.terraform.io/providers/hashicorp/aws/4.22.0/docs/resources/cloudwatch_event_target) | resource |
| [aws_iam_policy.lambda_tagging_policy](https://registry.terraform.io/providers/hashicorp/aws/4.22.0/docs/resources/iam_policy) | resource |
| [aws_iam_role.lambda_function_role](https://registry.terraform.io/providers/hashicorp/aws/4.22.0/docs/resources/iam_role) | resource |
| [aws_iam_role_policy_attachment.lambda_basic_policy](https://registry.terraform.io/providers/hashicorp/aws/4.22.0/docs/resources/iam_role_policy_attachment) | resource |
| [aws_iam_role_policy_attachment.lambda_tagging_policy](https://registry.terraform.io/providers/hashicorp/aws/4.22.0/docs/resources/iam_role_policy_attachment) | resource |
| [aws_lambda_permission.event_rule](https://registry.terraform.io/providers/hashicorp/aws/4.22.0/docs/resources/lambda_permission) | resource |
| [aws_resourcegroups_group.resource_group](https://registry.terraform.io/providers/hashicorp/aws/4.22.0/docs/resources/resourcegroups_group) | resource |
| [aws_caller_identity.current](https://registry.terraform.io/providers/hashicorp/aws/4.22.0/docs/data-sources/caller_identity) | data source |
| [aws_iam_role.lambda_function_role](https://registry.terraform.io/providers/hashicorp/aws/4.22.0/docs/data-sources/iam_role) | data source |
| [aws_region.current](https://registry.terraform.io/providers/hashicorp/aws/4.22.0/docs/data-sources/region) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_aws_region"></a> [aws\_region](#input\_aws\_region) | The AWS region to use | `string` | `"us-east-1"` | no |
| <a name="input_enable_cloudwatch_dashboard"></a> [enable\_cloudwatch\_dashboard](#input\_enable\_cloudwatch\_dashboard) | Enable the CloudWatch Dashboard | `bool` | `false` | no |
| <a name="input_lambda_function_name"></a> [lambda\_function\_name](#input\_lambda\_function\_name) | The name of the Lambda function | `string` | `"AWSAutoTaggingFunction"` | no |
| <a name="input_lambda_function_role_name"></a> [lambda\_function\_role\_name](#input\_lambda\_function\_role\_name) | The name of the Lambda function role | `string` | `"AWSAutoTaggingFunctionRole"` | no |
| <a name="input_resource_tags"></a> [resource\_tags](#input\_resource\_tags) | Tags to apply to resources | `map(string)` | `null` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_completed_region"></a> [completed\_region](#output\_completed\_region) | The region that the Lambda function was created |
<!-- END_TF_DOCS -->
