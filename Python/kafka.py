#!/usr/bin/env python3
import boto3
import json
import sys
import datetime
from optparse import OptionParser

### Arguments
parser = OptionParser()
parser.add_option("-a", "--account", dest="profile", default="", help="aws-account-profile-name")
parser.add_option("-r", "--region", dest="region", default="", help="RDS region")
parser.add_option("-n", "--arn", dest="arn", default="", help="Kafka Cluster ARN")
parser.add_option("-c", "--clustername", dest="clsname", default="", help="Kafka Cluster Name")
(options, args) = parser.parse_args()

if (options.profile == None):
    parser.error("-a aws account name is required")
if (options.arn == None):
    parser.error("-n kafka cluster arn is required")
if (options.clsname == None):
    parser.error("-c kafka cluster name is required")

boto3.setup_default_session(profile_name=options.profile)
acc = boto3.client('sts').get_caller_identity().get('Account')
client = boto3.client('kafka', options.region)
res = client.describe_cluster(ClusterArn='arn:aws:kafka:' + options.region + ':' + acc + ':cluster/' + options.arn)
state = res['ClusterInfo']['State']

end = datetime.datetime.utcnow()
start = end - datetime.timedelta(minutes=5)
cw = boto3.client('cloudwatch', options.region)
kafcw = []
metricsum = ["ActiveControllerCount", "GlobalPartitionCount", "GlobalTopicCount", "OfflinePartitionsCount", "ZooKeeperRequestLatencyMsMean", "ZooKeeperSessionState"]
metricavg = ["KafkaDataLogsDiskUsed"]
for m in range(len(metricsum)):
    res = cw.get_metric_statistics(Namespace='AWS/Kafka', MetricName=metricsum[m], StartTime=start, EndTime=end, Period=60, Statistics=["Sum"], Dimensions=[{'Name': "Cluster Name", 'Value': options.clsname}])
    datapoints = res.get('Datapoints')
    average = datapoints[-1].get('Sum')
    kafcw.append(average)
for m in range(len(metricavg)):
    res = cw.get_metric_statistics(Namespace='AWS/Kafka', MetricName=metricavg[m], StartTime=start, EndTime=end, Period=60, Statistics=["Average"], Dimensions=[{'Name': "Cluster Name", 'Value': options.clsname}])
    datapoints = res.get('Datapoints')
    average = datapoints[-1].get('Average')
    kafcw.append(average)
stats = {"ClusterState": state, "ActiveControllerCount": kafcw[0], "GlobalPartitionCount": kafcw[1], "GlobalTopicCount": kafcw[2], "OfflinePartitionsCount": kafcw[3], "ZooKeeperRequestLatencyMsMean": kafcw[4], "ZooKeeperSessionState": kafcw[5], "KafkaDataLogsDiskUsed": kafcw[6]}
print(json.dumps(stats))
