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
parser.add_option("-n", "--name", dest="name",
                help="Elasticache Cluster name")
parser.add_option("-e", "--EcId", dest="EcId",
                help="Elasticache Cluster Id")
parser.add_option("-c", "--clsstat", dest="clsstat",
                help="Elasticache Cluster status")
parser.add_option("-p", "--pmstat", dest="pmstat",
                help="Elasticache Parameter Apply status")
(options, args) = parser.parse_args()

if (options.profile == None):
    parser.error("-a aws account name is required")

boto3.setup_default_session(profile_name=options.profile)
client = boto3.client('elasticache', options.region)

#ElastiCache Discovery
if (options.EcId == None):
    res = client.describe_cache_clusters()
    cls_dict = {}
    cls_list = []
    names = [d['CacheClusterId'] for d in res['CacheClusters'] if isinstance(d, dict) and 'CacheClusterId' in d]
    for match in names:
        if options.name in match:
            clsid = { "{#CLSID}": match }
            cls_list.append(clsid)
            cls_dict['data'] = cls_list
    print(json.dumps(cls_dict))
#Get cluster level basic info
else:
    res = client.describe_cache_clusters(CacheClusterId=options.EcId)
    node = res['CacheClusters'][0]['CacheNodeType']
    engine = res['CacheClusters'][0]['Engine']
    stat = res['CacheClusters'][0]['CacheClusterStatus']
    pas = res['CacheClusters'][0]['CacheParameterGroup']['ParameterApplyStatus']
    tee = res['CacheClusters'][0]['TransitEncryptionEnabled']
    ree = res['CacheClusters'][0]['AtRestEncryptionEnabled']
    stats = {"CacheNodeType": node, "Engine": engine, "CacheClusterStatus": stat, "ParameterApplyStatus": pas, "TransitEncryptionEnabled": tee, "AtRestEncryptionEnabled": ree}
#    print(json.dumps(stats))
    if (options.clsstat != None):
        print(stat)
    if (options.pmstat !=None):
        print(pas)
