locals {
  lambda_assumed_event = "arn:aws:sts::${data.aws_caller_identity.current.account_id}:assumed-role/${var.lambda_function_role_name}/${module.lambda.lambda_function_name}"
  event_pattern = [
    {
      service    = "EC2"
      source     = ["aws.ec2"]
      event_name = [{ "prefix" = "Create" }, { "prefix" = "Copy" }, "RunInstances", "AllocateAddress"]
    },
    {
      service    = "ELB"
      source     = ["aws.elasticloadbalancing"]
      event_name = ["CreateLoadBalancer", "CreateTargetGroup"]
    },
    {
      service    = "RDS"
      source     = ["aws.rds"]
      event_name = [{ "prefix" = "Create" }]
    },
    {
      service    = "CloudFront"
      source     = ["aws.cloudfront"]
      event_name = ["CreateDistribution"]
    },
    {
      service    = "SNS"
      source     = ["aws.sns"]
      event_name = [{ "prefix" = "Create" }]
    },
    {
      service    = "Lambda"
      source     = ["aws.lambda"]
      event_name = [{ "prefix" = "Create" }]
    },
    {
      service    = "IAM"
      source     = ["aws.iam"]
      event_name = ["CreateRole", "CreatePolicy"]
    },
    {
      service    = "AutoScaling"
      source     = ["aws.autoscaling"]
      event_name = ["CreateAutoScalingGroup"]
    }
  ]
}

resource "aws_cloudwatch_event_rule" "event_rule" {
  count       = length(local.event_pattern)
  name        = "AWSAutoTaggingEventRule${local.event_pattern[count.index].service}"
  description = "Get the CloudTrail event from ${local.event_pattern[count.index].service}"
  tags        = var.resource_tags
  event_pattern = jsonencode(
    {
      "source" : "${local.event_pattern[count.index].source}",
      "detail" : {
        "userIdentity" : {
          "arn" : [{
            "anything-but" : "${local.lambda_assumed_event}"
          }]
        },
        "eventName" : "${local.event_pattern[count.index].event_name}"
      }
    }
  )
}

resource "aws_cloudwatch_event_target" "event_rule" {
  count = length(local.event_pattern)
  rule  = aws_cloudwatch_event_rule.event_rule[count.index].name
  arn   = module.lambda.lambda_function_arn
}

resource "aws_lambda_permission" "event_rule" {
  count         = length(local.event_pattern)
  statement_id  = aws_cloudwatch_event_rule.event_rule[count.index].name
  action        = "lambda:InvokeFunction"
  function_name = module.lambda.lambda_function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.event_rule[count.index].arn
}
