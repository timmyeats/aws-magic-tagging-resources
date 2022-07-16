import re
import datetime


def get_identity_type(event, tags):
    tags["UserType"] = event["detail"]["userIdentity"]["type"]

    if tags["UserType"] == "AssumedRole":
        tags["Owner"] = event["detail"]["userIdentity"]["principalId"].split(":")[1]
        tags["RoleName"] = event["detail"]["userIdentity"]["sessionContext"]["sessionIssuer"]["userName"]

    elif tags["UserType"] == "IAMUser":
        tags["Owner"] = event["detail"]["userIdentity"]["userName"]

    elif tags["UserType"] == "Root":
        tags["Owner"] = "Root"

    else:
        return None

    return tags


# Get resource event time and convert to UTC timezone
def get_event_time(event, tags, utc_time=0):
    event_time = datetime.datetime.strptime(event["detail"]["eventTime"], "%Y-%m-%dT%H:%M:%SZ")
    event_time = event_time + datetime.timedelta(hours=utc_time)
    event_time = event_time.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=utc_time)))
    tags["EventTime"] = event_time.strftime("%Y-%m-%dT%H:%M:%S%z")
    return tags


# Response elements data processing
def response_elements_data_processing(response_elements, regular_expression):
    keys, values = [], []
    for key, value in response_elements.items():
        keys.append(key)
        values.append(value)

        try:
            if type(value) == dict:
                for key, value in value.items():
                    keys.append(key)
                    values.append(value)

            if type(value) == list:
                for key, value in value[0].items():
                    keys.append(key)
                    values.append(value)
        except:
            continue

    # Get values from response elements
    for value in values:
        resource = re.match(regular_expression, str(value), flags=0)
        if resource != None:
            return resource.group(0)

    return None


# Get resource id from event
def get_resource_id(response_elements):
    regular_expression = "[a-z]*?-.*"
    resource_id = response_elements_data_processing(response_elements, regular_expression)
    return resource_id


# Get resource arn from event
def get_resource_arn(response_elements):
    regular_expression = "arn\:aws\:.*"
    resource_arn = response_elements_data_processing(response_elements, regular_expression)
    return resource_arn


# Changing a tag to an array tag
def changing_tag_to_array(tags):
    tags_array = []
    for key, value in tags.items():
        tags_array.append({"Key": key, "Value": value})
    return tags_array   
