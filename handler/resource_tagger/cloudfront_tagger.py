import boto3
from .taggers import get_resource_arn


# Create tags for AWS resources
def add_tags_in_resource(tags, resource, add_tags=[]):
    for tag_key, tag_value in tags.items():
        add_tags.append({"Key": tag_key, "Value": tag_value})

    try:
        client = boto3.client("cloudfront")
        response = client.tag_resource(
            Resource=resource,
            Tags={
                "Items": add_tags
            }
        )

    except Exception as e:
        response = {"[LOG] Error: ": str(e)}

    return response, add_tags


def tagger(event, tags, resource_arn=None):
    response_elements = event["detail"]["responseElements"]

    if event["detail"]["eventName"] == None:
        resource_arn = None

    else:
        resource_arn = get_resource_arn(response_elements)

    if resource_arn != None:
        response, tags = add_tags_in_resource(tags, resource_arn)
        response["resource_arn"] = resource_arn
        response["tags"] = tags
        return response

    else:
        return "[LOG] No resource arn found!"
