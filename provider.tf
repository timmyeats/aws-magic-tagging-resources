data "aws_caller_identity" "current" {}

terraform {
  required_version = ">= 0.14"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.22.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}
