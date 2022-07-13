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
