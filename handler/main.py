import resource_tagger.ec2_tagger as ec2_tagger
import resource_tagger.elb_tagger as elb_tagger
import resource_tagger.rds_tagger as rds_tagger
import resource_tagger.cloudfront_tagger as cf_tagger
import resource_tagger.sns_tagger as sns_tagger
import resource_tagger.lambda_tagger as lambda_tagger
import resource_tagger.iam_tagger as iam_tagger
import resource_tagger.autoscaling_tagger as asg_tagger
import resource_tagger.taggers as taggers


# Get tag information from event
def get_tag_information(event, tags={}):
    print("[Event]", event)
    tags["SourceIP"] = event["detail"]["sourceIPAddress"]
    tags["EventTime"] = event["detail"]["eventTime"]
    if event["detail"]["userAgent"] != "AWS Internal":
        print("[UserAgent]", event["detail"]["userAgent"])
    tags = taggers.get_event_time(event, tags, utc_time=8)
    tags = taggers.get_identity_type(event, tags)
    return tags


# Create tags for AWS resources
def lambda_handler(event, context):
    tags = get_tag_information(event)

    if tags != None:
        if event["source"] == "aws.ec2":
            response = ec2_tagger.tagger(event, tags)

        elif event["source"] == "aws.elasticloadbalancing":
            response = elb_tagger.tagger(event, tags)

        elif event["source"] == "aws.rds":
            response = rds_tagger.tagger(event, tags)
            
        elif event["source"] == "aws.cloudfront":
            response = cf_tagger.tagger(event, tags)

        elif event["source"] == "aws.sns":
            response = sns_tagger.tagger(event, tags)

        elif event["source"] == "aws.lambda":
            response = lambda_tagger.tagger(event, tags)

        elif event["source"] == "aws.iam":
            response = iam_tagger.tagger(event, tags)

        elif event["source"] == "aws.autoscaling":
            print("[LOG] Autoscaling tagger")
            response = asg_tagger.tagger(event, tags)

        else:
            response = "[LOG] No support source found!"
    else:
        response = "[LOG] No tags found!"
    
    print(response)
    return response
