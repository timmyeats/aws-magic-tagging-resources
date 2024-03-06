locals {
  dashboard_query = <<-EOT
    SOURCE '/aws/lambda/${var.lambda_function_name}'
    | fields @timestamp, @message
    | filter @message not like 'START RequestId'
    | filter @message not like 'REPORT RequestId'
    | filter @message not like 'END RequestId'
    | filter @message not like 'INIT_START'
    | sort @timestamp desc
    | limit 100
    EOT
  dashboard_widget_regions = [
    "us-east-1",
    "us-east-2",
    "us-west-1",
    "us-west-2",
    "ap-northeast-1",
    "ap-southeast-1",
  ]
}

resource "aws_cloudwatch_dashboard" "dashboard" {
  count          = terraform.workspace == "default" && var.enable_cloudwatch_dashboard ? 1 : 0
  dashboard_name = "AWSAutoTaggingDashboard"
  dashboard_body = jsonencode(
    {
      "widgets" : [
        {
          "type" : "log",
          "x" : 0,
          "y" : 0,
          "width" : 12,
          "height" : 6,
          "properties" : {
            "region" : "${local.dashboard_widget_regions[0]}",
            "title" : "/aws/lambda/${var.lambda_function_name} (${local.dashboard_widget_regions[0]})",
            "query" : "${local.dashboard_query}",
            "view" : "table"
          }
        },
        {
          "type" : "log",
          "x" : 12,
          "y" : 0,
          "width" : 12,
          "height" : 6,
          "properties" : {
            "region" : "${local.dashboard_widget_regions[1]}",
            "title" : "/aws/lambda/${var.lambda_function_name} (${local.dashboard_widget_regions[1]})",
            "query" : "${local.dashboard_query}",
            "view" : "table"
          }
        },
        {
          "type" : "log",
          "x" : 0,
          "y" : 6,
          "width" : 12,
          "height" : 6,
          "properties" : {
            "region" : "${local.dashboard_widget_regions[2]}",
            "title" : "/aws/lambda/${var.lambda_function_name} (${local.dashboard_widget_regions[2]})",
            "query" : "${local.dashboard_query}",
            "view" : "table"
          }
        },
        {
          "type" : "log",
          "x" : 12,
          "y" : 6,
          "width" : 12,
          "height" : 6,
          "properties" : {
            "region" : "${local.dashboard_widget_regions[3]}",
            "title" : "/aws/lambda/${var.lambda_function_name} (${local.dashboard_widget_regions[3]})",
            "query" : "${local.dashboard_query}",
            "view" : "table"
          }
        },
        {
          "type" : "log",
          "x" : 0,
          "y" : 12,
          "width" : 12,
          "height" : 6,
          "properties" : {
            "region" : "${local.dashboard_widget_regions[4]}",
            "title" : "/aws/lambda/${var.lambda_function_name} (${local.dashboard_widget_regions[4]})",
            "query" : "${local.dashboard_query}",
            "view" : "table"
          }
        },
        {
          "type" : "log",
          "x" : 12,
          "y" : 12,
          "width" : 12,
          "height" : 6,
          "properties" : {
            "region" : "${local.dashboard_widget_regions[5]}",
            "title" : "/aws/lambda/${var.lambda_function_name} (${local.dashboard_widget_regions[5]})",
            "query" : "${local.dashboard_query}",
            "view" : "table"
          }
        },
      ]
    }
  )
}
