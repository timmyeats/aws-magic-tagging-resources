module "lambda" {
  source        = "terraform-aws-modules/lambda/aws"
  version       = "3.3.1"
  function_name = "AWSAutoTaggingFunction"
  description   = "The auto-tagging lambda function for AWS resources"
  handler       = "main.lambda_handler"
  runtime       = "python3.9"
  source_path   = "./handler"
  memory_size   = 128
  timeout       = 30
  create_role   = false
  lambda_role   = aws_iam_role.lambda_function_role.arn
  tags          = var.resource_tags
}
