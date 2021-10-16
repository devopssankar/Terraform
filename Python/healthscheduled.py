#!/usr/bin/env python3
import boto3
import json
import sys
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-a", "--account", dest="profile",
                        help="aws-account-profile-name")
parser.add_option("-r", "--region", dest="region", default="us-east-1",
                                help="AWS region")
(options, args) = parser.parse_args()

if (options.profile == None):
    parser.error("-a aws account name is required")

try:
    boto3.setup_default_session(profile_name=options.profile)
    client = boto3.client('health','us-east-1') #https://docs.aws.amazon.com/health/latest/ug/health-api.html
    eventarn = client.describe_events(filter={'regions':[str(options.region)],'eventTypeCategories':['scheduledChange'],'eventStatusCodes':['upcoming']})['events']
    if (eventarn != []):
        eventarn = client.describe_events(filter={'regions':[str(options.region)],'eventTypeCategories':['scheduledChange'],'eventStatusCodes':['upcoming']})['events'][0]['arn']
        affected = client.describe_affected_entities(filter={'eventArns': [str(eventarn)]})['entities'][0]['entityValue']
        tz = "UTC" if (options.region == 'us-east-1') else "GMT"
        eventmsg = client.describe_event_details(eventArns=[str(eventarn)])['successfulSet'][0]['eventDescription']['latestDescription'].split(str(tz), 1)[0]
        print("AWS Resource affected: " + affected,'\n',eventmsg + tz)
    else:
        print("NoScheduledEvents")
except:
    raise
