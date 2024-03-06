import boto3

from .taggers import changing_tag_to_array
from .taggers import get_resource_arn


# Create tags for AWS resources
def add_tags_in_resource(tags, resource):
    converted_tags = changing_tag_to_array(tags)
    try:
        client = boto3.client("cloudfront")
        response = client.tag_resource(
            Resource=resource,
            Tags={"Items": converted_tags},
        )
    except Exception as e:
        response = {"[LOG] Error: ": str(e)}

    return response, converted_tags


def add_comment_in_cloudfront(tags, resource, response=None):
    distribution_id = resource.split("/")[1]
    client = boto3.client("cloudfront")
    distribution_config = client.get_distribution_config(Id=distribution_id)

    if distribution_config["DistributionConfig"]["Comment"] == "":
        distribution_config["DistributionConfig"]["Comment"] = (
            "Created by " + tags["Owner"]
        )
        response = client.update_distribution(
            Id=distribution_id,
            DistributionConfig=distribution_config["DistributionConfig"],
            IfMatch=distribution_config["ETag"],
        )
    else:
        response = "[LOG] Distribution already has a comment!"

    print(response)
    return


def tagger(event, tags, resource_arn=None):
    response_elements = event["detail"]["responseElements"]

    if event["detail"]["eventName"] == None:
        resource_arn = None

    else:
        resource_arn = get_resource_arn(response_elements)

    if resource_arn != None:
        add_comment_in_cloudfront(tags, resource_arn)
        response, converted_tags = add_tags_in_resource(tags, resource_arn)
        response["resource_arn"] = resource_arn
        response["converted_tags"] = converted_tags
        return response

    else:
        return "[LOG] No resource arn found!"
