#!/usr/bin/env python3
import boto3
import json
import sys
from optparse import OptionParser
import datetime

# Arguments
parser = OptionParser()
parser.add_option("-a", "--account", dest="profile",
                help="aws-account-profile-name")
parser.add_option("-r", "--region", dest="region", default="us-east-1",
                help="Region")
parser.add_option("-n", "--esname", dest="esname",
                help="Elasticsearch Service Domain Name")
(options, args) = parser.parse_args()

if (options.profile == None):
    parser.error("-a aws account name is required")
if (options.esname == None):
    parser.error("-n Elasticsearch service domain name is required")

#Elasticsearch domain ClientId mapping
if (options.profile == "sankar-prod"):
    clientId = "222222222222"
if (options.profile == "sankar-stg"):
    clientId = "111111111111"

#Collect ES Cloudwatch Metrics in one go
end = datetime.datetime.utcnow()
start = end - datetime.timedelta(minutes=5)

boto3.setup_default_session(profile_name=options.profile)
cw = boto3.client('cloudwatch', options.region)
es_metric = []
metric = ["ClusterStatus.green", "Nodes", "SearchableDocuments", "CPUUtilization", "FreeStorageSpace", "ClusterUsedSpace", "ClusterIndexWritesBlocked",
          "JVMMemoryPressure", "KibanaHealthyNodes", "ElasticsearchRequests", "2xx", "3xx", "4xx", "5xx", "SearchRate", "IndexingRate"]
for m in range(len(metric)):
    res = cw.get_metric_statistics(Namespace='AWS/ES', MetricName=metric[m], StartTime=start, EndTime=end, Period=60, Statistics=["Maximum"],
                                   Dimensions=[{'Name': "ClientId", 'Value': clientId}, {'Name': "DomainName", 'Value': options.esname}])
    datapoints = res.get('Datapoints')
    average = datapoints[-1].get('Maximum')
    if (metric[m] == "FreeStorageSpace" or metric[m] == "ClusterUsedSpace"):
        average = average * 1024.0 * 1024.0
    es_metric.append(average)
stats = {"ClusterStatus": es_metric[0], "Nodes": es_metric[1], "SearchableDocuments": es_metric[2], "CPUUtilization": es_metric[3], "FreeStorageSpace": es_metric[4],
         "ClusterUsedSpace": es_metric[5], "ClusterIndexWritesBlocked": es_metric[6], "JVMMemoryPressure": es_metric[7], "KibanaHealthyNodes": es_metric[8],
         "ElasticsearchRequests": es_metric[9], "2xx": es_metric[10], "3xx": es_metric[11], "4xx": es_metric[12], "5xx": es_metric[13], "SearchRate": es_metric[14],
         "IndexingRate": es_metric[15]}
print(json.dumps(stats))
