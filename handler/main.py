import resource_tagger.ec2_tagger as ec2_tagger
import resource_tagger.elb_tagger as elb_tagger
import resource_tagger.taggers as taggers


# Get tag information from event
def get_tag_information(event, tags={}):
    print(event)
    tags["SourceIP"] = event["detail"]["sourceIPAddress"]
    tags["EventTime"] = event["detail"]["eventTime"]
    tags = taggers.get_event_time(event, tags, utc_time=8)
    tags = taggers.get_identity_type(event, tags)
    return tags


# Create tags for AWS resources
def lambda_handler(event, context):
    tags = get_tag_information(event)

    if tags != None:
        if event["source"] == "aws.ec2":
            response = ec2_tagger.tagger(event, tags)
            print(response)

        elif event["source"] == "aws.elasticloadbalancing":
            response = elb_tagger.tagger(event, tags)
            print(response)

        else:
            print("[LOG] No support source found!")

    else:
        print("[LOG] Tags not found!")
