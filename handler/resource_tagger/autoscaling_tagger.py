import boto3
from .taggers import changing_tag_to_array    


# Create tags for AWS resources
def add_tags_in_resource(tags, resource):
    asg_add_tags = []
    converted_tags = changing_tag_to_array(tags)

    try:
        for tag in converted_tags:
            tag["ResourceId"] = resource
            tag["ResourceType"] = "auto-scaling-group"
            tag["PropagateAtLaunch"] = True
            asg_add_tags.append(tag)
        client = boto3.client("autoscaling")
        response = client.create_or_update_tags(
            Tags=asg_add_tags
        )
    except Exception as e:
        response = {"[LOG] Error: ": str(e)}

    return response, converted_tags


def tagger(event, tags):
    request_parameters = event["detail"]["requestParameters"]
    autoscaling_group_name = request_parameters["autoScalingGroupName"]

    if autoscaling_group_name is not None:
        response, tags = add_tags_in_resource(tags, autoscaling_group_name)
        response["autoscaling_group_name"] = autoscaling_group_name
        response["tags"] = tags
        return response

    else:
        return "[LOG] No resource id found!"
