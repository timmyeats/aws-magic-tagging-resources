locals {
  lambda_function_role_name = "AWSAutoTaggingFunctionRole"
}

data "aws_iam_role" "lambda_function_role" {
  count = terraform.workspace == "default" ? 0 : 1
  name  = local.lambda_function_role_name
}

resource "aws_iam_role" "lambda_function_role" {
  count       = terraform.workspace == "default" ? 1 : 0
  name        = local.lambda_function_role_name
  description = "Allow Lambda to tag resources"
  tags        = var.resource_tags
  assume_role_policy = jsonencode(
    {
      Version = "2012-10-17"
      Statement = [
        {
          Action = "sts:AssumeRole"
          Effect = "Allow"
          Sid    = ""
          Principal = {
            Service = "lambda.amazonaws.com"
          }
        }
      ]
    }
  )
}

resource "aws_iam_role_policy_attachment" "lambda_basic_permission" {
  count      = terraform.workspace == "default" ? 1 : 0
  role       = aws_iam_role.lambda_function_role[count.index].name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "lambda_tagging_policy" {
  count      = terraform.workspace == "default" ? 1 : 0
  role       = aws_iam_role.lambda_function_role[count.index].name
  policy_arn = aws_iam_policy.lambda_tagging_policy[count.index].arn
}

resource "aws_iam_policy" "lambda_tagging_policy" {
  count       = terraform.workspace == "default" ? 1 : 0
  name        = "AWSAutoTaggingFunctionPolicy"
  description = "Allow Lambda to tag resources"
  tags        = var.resource_tags
  policy = jsonencode(
    {
      "Version" : "2012-10-17",
      "Statement" : [
        {
          "Sid" : "VisualEditor0",
          "Effect" : "Allow",
          "Action" : [
            "ec2:*Tag*",
            "elasticloadbalancing:*Tag*"
          ],
          "Resource" : "*"
        }
      ]
    }
  )
}
