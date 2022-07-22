variable "aws_region" {
  default     = "us-east-1"
  type        = string
  description = "The AWS region to use"
}

variable "resource_tags" {
  default     = null
  type        = map(string)
  description = "Tags to apply to resources"
}

variable "lambda_function_name" {
  default     = "AWSAutoTaggingFunction"
  type        = string
  description = "The name of the Lambda function"
}

variable "lambda_function_role_name" {
  default     = "AWSAutoTaggingFunctionRole"
  type        = string
  description = "The name of the Lambda function role"
}

variable "enable_cloudwatch_dashboard" {
  default     = false
  type        = bool
  description = "Enable the CloudWatch Dashboard"
}