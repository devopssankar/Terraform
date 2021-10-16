#!/usr/bin/env python3
import boto3
import json
import sys
from optparse import OptionParser

### Arguments
parser = OptionParser()
parser.add_option("-a", "--account", dest="profile",
                        help="aws-account-profile-name")
parser.add_option("-r", "--region", dest="region", default="us-east-1",
                                help="RDS region")
parser.add_option("-e", "--envname", dest="EnvironmentName",
                        help="Elastic Beanstalk EnvironmentName")
parser.add_option("-i", "--instances", dest="inshealth",
                        help="Instances health check")
(options, args) = parser.parse_args()
if (options.profile == None):
    parser.error("-a aws account name is required")
if (options.EnvironmentName == None):
    parser.error("-e Elastic Beanstalk EnvironmentName is required")

boto3.setup_default_session(profile_name=options.profile)

try:
    eb = boto3.client('elasticbeanstalk',options.region)
    if (options.inshealth != None):
        res = eb.describe_instances_health(EnvironmentName=options.EnvironmentName,AttributeNames=['InstanceType'])
        print(json.dumps(res))
    else:
        eb_dict = {}
        eb_list = []
        res = eb.describe_environment_health(EnvironmentName=options.EnvironmentName,AttributeNames=['All'])
        health = res['HealthStatus']
        causes = res['Causes']
        appmetric = res['ApplicationMetrics']
        healthcauses = {"HealthStatus": health, "Causes": causes}
        eb_list.append(healthcauses)
        eb_list.append(appmetric)
        eb_dict['data'] = eb_list
        print(json.dumps(eb_dict))
except:
    raise
