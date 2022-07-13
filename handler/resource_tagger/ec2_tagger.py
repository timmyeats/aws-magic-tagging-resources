import boto3
from .taggers import get_resource_id


# Create tags for AWS resources
def add_tags_in_resource(tags, resource, add_tags=[]):
    for tag_key, tag_value in tags.items():
        add_tags.append({"Key": tag_key, "Value": tag_value})

    try:
        client = boto3.client("ec2")
        response = client.create_tags(
            Resources=[resource],
            Tags=add_tags
        )
    except Exception as e:
        response = {"[LOG] Error: ": str(e)}

    return response, add_tags


def tagger(event, tags, resource_id=None):
    response_elements = event["detail"]["responseElements"]

    if event["detail"]["eventName"] == "RunInstances":
        resource_id = response_elements["instancesSet"]["items"][0]["instanceId"]

    elif event["detail"]["eventName"] == "CreateManagedPrefixList":
        resource_id = response_elements["CreateManagedPrefixListResponse"]["prefixList"]["prefixListId"]

    elif event["detail"]["eventName"] == "CreateNatGateway":
        resource_id = response_elements["CreateNatGatewayResponse"]["natGateway"]["natGatewayId"]

    else:
        resource_id = get_resource_id(response_elements)

    if resource_id != None:
        response, tags = add_tags_in_resource(tags, resource_id)
        response["resource_id"] = resource_id
        response["tags"] = tags
        return response

    else:
        return "[LOG] No resource id found!"
