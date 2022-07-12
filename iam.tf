resource "aws_iam_role" "lambda_function_role" {
  name        = "AWSAutoTaggingFunctionRole"
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
  role       = aws_iam_role.lambda_function_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "lambda_tagging_policy" {
  role       = aws_iam_role.lambda_function_role.name
  policy_arn = aws_iam_policy.lambda_tagging_policy.arn
}

resource "aws_iam_policy" "lambda_tagging_policy" {
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
