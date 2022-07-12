variable "aws_region" {
  type        = string
  description = "The AWS region to use"
}

variable "resource_tags" {
  default     = null
  type        = map(string)
  description = "Tags to apply to resources"
}
