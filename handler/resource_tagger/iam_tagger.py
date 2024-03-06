import boto3

from .taggers import changing_tag_to_array
from .taggers import get_resource_arn


# Create tags for AWS resources
def add_tags_in_resource(tags, resource):
    converted_tags = changing_tag_to_array(tags)
    try:
        client = boto3.client("iam")
        response = client.tag_policy(PolicyArn=resource, Tags=converted_tags)
    except Exception as e:
        response = {"[LOG] Error: ": str(e)}

    return response, converted_tags


def add_tags_in_role(tags, resource):
    converted_tags = changing_tag_to_array(tags)
    try:
        client = boto3.client("iam")
        response = client.tag_role(RoleName=resource, Tags=converted_tags)
    except Exception as e:
        response = {"[LOG] Error: ": str(e)}

    return response, converted_tags


def tagger(event, tags, response=None):
    response_elements = event["detail"]["responseElements"]

    if event["detail"]["eventName"] == "CreateRole":
        resource_name = response_elements["role"]["roleName"]
        response, converted_tags = add_tags_in_role(tags, resource_name)
        response["resource_name"] = resource_name

    elif event["detail"]["eventName"] == "CreatePolicy":
        resource_arn = get_resource_arn(response_elements)
        response, converted_tags = add_tags_in_resource(tags, resource_arn)
        response["resource_arn"] = resource_arn

    else:
        return "[LOG] No resource arn found!"

    response["converted_tags"] = converted_tags
    return response
