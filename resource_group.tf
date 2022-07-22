resource "aws_resourcegroups_group" "resource_group" {
  name        = "AutoTaggingResourceGroup"
  description = "The auto-tagging resource group for AWS resources"
  resource_query {
    query = jsonencode(
      {
        "ResourceTypeFilters" : [
          "AWS::AllSupported"
        ],
        "TagFilters" : [
          {
            "Key" : "Owner",
          },
          {
            "Key" : "EventTime",
          }
        ]
      }
    )
  }
}