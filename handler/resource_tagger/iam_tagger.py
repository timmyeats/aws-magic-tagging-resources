import boto3
from .taggers import get_resource_arn
from .taggers import changing_tag_to_array


# Create tags for AWS resources
def add_tags_in_resource(tags, resource):
    add_tags = changing_tag_to_array(tags)
    try:
        client = boto3.client("iam")
        response = client.tag_policy(
            PolicyArn=resource,
            Tags=add_tags
        )
    except Exception as e:
        response = {"[LOG] Error: ": str(e)}

    return response, add_tags


def add_tags_in_role(tags, resource):
    add_tags = changing_tag_to_array(tags)
    try:
        client = boto3.client("iam")
        response = client.tag_role(
            RoleName=resource,
            Tags=add_tags
        )
    except Exception as e:
        response = {"[LOG] Error: ": str(e)}

    return response, add_tags


def tagger(event, tags, response=None):
    response_elements = event["detail"]["responseElements"]

    if event["detail"]["eventName"] == "CreateRole":
        resource_name = response_elements["role"]["roleName"]
        response, tags = add_tags_in_role(tags, resource_name)
        response["resource_name"] = resource_name
        
    elif event["detail"]["eventName"] == "CreatePolicy":
        resource_arn = get_resource_arn(response_elements)
        response, tags = add_tags_in_resource(tags, resource_arn)
        response["resource_arn"] = resource_arn
    
    else:
        return "[LOG] No resource arn found!"

    response["tags"] = tags
    return response
