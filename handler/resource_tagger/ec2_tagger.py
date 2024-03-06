import boto3

from .taggers import changing_tag_to_array
from .taggers import get_resource_id


# Get EBS VolumeIds
def get_ebs_volume_ids(instance_id):
    volume_ids = []
    client = boto3.client("ec2")
    response = client.describe_instances(InstanceIds=[instance_id])
    for instance in response["Reservations"][0]["Instances"]:
        for block_device in instance["BlockDeviceMappings"]:
            volume_ids.append(block_device["Ebs"]["VolumeId"])
    return volume_ids


# Get AMI SnapshotIds
def get_ami_snapshot_id(ami_id):
    snapshot_ids = []
    client = boto3.client("ec2")
    response = client.describe_images(ImageIds=[ami_id])
    for ebs_mapping in response["Images"][0]["BlockDeviceMappings"]:
        snapshot_ids.append(ebs_mapping["Ebs"]["SnapshotId"])
    return snapshot_ids


# Create tags for AWS resources
def add_tags_in_resource(tags, resource):
    converted_tags = changing_tag_to_array(tags)

    try:
        client = boto3.client("ec2")
        response = client.create_tags(Resources=[resource], Tags=converted_tags)
    except Exception as e:
        response = {"[LOG] Error: ": str(e)}

    return response, converted_tags


def tagger(event, tags, resource_id=None):
    event_name = event["detail"]["eventName"]
    response_elements = event["detail"]["responseElements"]

    if event_name == "RunInstances":
        resource_id = response_elements["instancesSet"]["items"][0]["instanceId"]

    elif event_name == "CreateManagedPrefixList":
        resource_id = response_elements["CreateManagedPrefixListResponse"][
            "prefixList"
        ]["prefixListId"]

    elif event_name == "CreateNatGateway":
        resource_id = response_elements["CreateNatGatewayResponse"]["natGateway"][
            "natGatewayId"
        ]

    else:
        resource_id = get_resource_id(response_elements)

    if event_name == "RunInstances" and resource_id is not None:
        response, converted_tags = add_tags_in_resource(tags, resource_id)
        volume_ids = get_ebs_volume_ids(resource_id)
        for volume_id in volume_ids:
            add_tags_in_resource(tags, volume_id)
        response["resource_id"] = resource_id
        response["converted_tags"] = converted_tags
        return response

    elif event_name == "CreateImage" and resource_id is not None:
        response, converted_tags = add_tags_in_resource(tags, resource_id)
        snapshot_ids = get_ami_snapshot_id(resource_id)
        for snapshot_id in snapshot_ids:
            add_tags_in_resource(tags, snapshot_id)
        response["resource_id"] = resource_id
        response["converted_tags"] = converted_tags
        return response

    elif resource_id is not None:
        response, converted_tags = add_tags_in_resource(tags, resource_id)
        response["resource_id"] = resource_id
        response["converted_tags"] = converted_tags
        return response

    else:
        return "[LOG] No resource id found!"
