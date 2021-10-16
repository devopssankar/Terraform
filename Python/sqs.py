#!/usr/bin/env python3
import boto3
import json
import sys
import datetime
from optparse import OptionParser

### Arguments
parser = OptionParser()
parser.add_option("-a", "--account", dest="profile",
                        help="AWS Account Name. for e.g. aws-account-profile-name")
parser.add_option("-r", "--region", dest="region", default="us-east-1",
                        help="SQS Region")
parser.add_option("-q", "--queue", dest="QueueName",
                        help="SQS Queue Name")
(options, args) = parser.parse_args()

if (options.profile == None):
    parser.error("-a aws account name is required")
if (options.QueueName == None):
    parser.error("-q SQS Queue Name is required")

end = datetime.datetime.utcnow()
start = end - datetime.timedelta(minutes=5)

boto3.setup_default_session(profile_name=options.profile)
cw = boto3.client('cloudwatch', options.region)
sqsmc = []
metric = ["ApproximateNumberOfMessagesDelayed", "NumberOfMessagesDeleted", "NumberOfMessagesReceived", "ApproximateAgeOfOldestMessage", "NumberOfEmptyReceives", "ApproximateNumberOfMessagesVisible", "ApproximateNumberOfMessagesNotVisible", "NumberOfMessagesSent"]
for m in range(len(metric)):
    res = cw.get_metric_statistics(Namespace='AWS/SQS', MetricName=metric[m], StartTime=start, EndTime=end, Period=60, Statistics=["Average"], Dimensions=[{'Name': "QueueName", 'Value': options.QueueName}])
    datapoints = res.get('Datapoints')
    average = datapoints[-1].get('Average')
    sqsmc.append(average)
stats = {"ApproximateNumberOfMessagesDelayed": sqsmc[0], "NumberOfMessagesDeleted": sqsmc[1], "NumberOfMessagesReceived": sqsmc[2], "ApproximateAgeOfOldestMessage": sqsmc[3], "NumberOfEmptyReceives": sqsmc[4], "ApproximateNumberOfMessagesVisible": sqsmc[5], "ApproximateNumberOfMessagesNotVisible": sqsmc[6], "NumberOfMessagesSent": sqsmc[7]}
print(json.dumps(stats))
