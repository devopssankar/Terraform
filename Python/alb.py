#!/usr/bin/env python3
import boto3
import json
import sys
from optparse import OptionParser
import datetime

# Arguments
parser = OptionParser()
parser.add_option("-a", "--account", dest="profile",
                help="account")
parser.add_option("-r", "--region", dest="region", default="us-east-1",
                help="region")
parser.add_option("-l", "--loadbalancer", dest="loadbalancer", 
                help="loadbalancer")
parser.add_option("-t", "--targetgroup", dest="targetgroup",
                help="targetgroup")
(options, args) = parser.parse_args()

if (options.profile == None):
    parser.error("-a aws account name is required. for e.g. aws-account-profile-name")
if (options.loadbalancer == None):
    parser.error("-l loadbalancer name is required. for e.g. sankar-lb/bdb040b5816a74e1") 
if (options.targetgroup == None):
    parser.error("-t targetgroup name is required. for e.g. sankar-lb-tg/db8cbbc26cf3e4a3")

try:
    boto3.setup_default_session(profile_name=options.profile)
    cw = boto3.client('cloudwatch', options.region)
    lb_metric = []
    end = datetime.datetime.utcnow() 
    start = end - datetime.timedelta(minutes=5)
    nc = cw.get_metric_statistics(Namespace='AWS/ApplicationELB', MetricName='NewConnectionCount', StartTime=start, EndTime=end, Period=60, Statistics=["Average"], Dimensions=[{'Name': "LoadBalancer", 'Value': 'app/' + options.loadbalancer}]).get('Datapoints')[-1].get('Average')
    lb_metric.append(round(nc))
    ac = cw.get_metric_statistics(Namespace='AWS/ApplicationELB', MetricName='ActiveConnectionCount', StartTime=start, EndTime=end, Period=60, Statistics=["Average"], Dimensions=[{'Name': "LoadBalancer", 'Value': 'app/' + options.loadbalancer}]).get('Datapoints')[-1].get('Average')
    lb_metric.append(round(ac))
    rt = cw.get_metric_statistics(Namespace='AWS/ApplicationELB', MetricName='TargetResponseTime', StartTime=start, EndTime=end, Period=60, Statistics=["Average"], Dimensions=[{'Name': "LoadBalancer", 'Value': 'app/' + options.loadbalancer}]).get('Datapoints')[-1].get('Average')
    lb_metric.append(round(rt,3))    
    rc = cw.get_metric_statistics(Namespace='AWS/ApplicationELB', MetricName='RequestCount', StartTime=start, EndTime=end, Period=60, Statistics=["Sum"], Dimensions=[{'Name': "LoadBalancer", 'Value': 'app/' + options.loadbalancer}]).get('Datapoints')[-1].get('Sum')
    lb_metric.append(round(rc))
    hh = cw.get_metric_statistics(Namespace='AWS/ApplicationELB', MetricName='HealthyHostCount', StartTime=start, EndTime=end, Period=60, Statistics=["Maximum"], Dimensions=[{'Name': "LoadBalancer", 'Value': 'app/' + options.loadbalancer}, {'Name': "TargetGroup", 'Value': 'targetgroup/' + options.targetgroup}]).get('Datapoints')[-1].get('Maximum')
    lb_metric.append(round(hh))
    uh = cw.get_metric_statistics(Namespace='AWS/ApplicationELB', MetricName='UnHealthyHostCount', StartTime=start, EndTime=end, Period=60, Statistics=["Maximum"], Dimensions=[{'Name': "LoadBalancer", 'Value': 'app/' + options.loadbalancer}, {'Name': "TargetGroup", 'Value': 'targetgroup/' + options.targetgroup}]).get('Datapoints')[-1].get('Maximum')
    lb_metric.append(round(uh))
    stats = {"NewConnectionCount": lb_metric[0], "ActiveConnectionCount": lb_metric[1], "TargetResponseTime": lb_metric[2], "RequestCount": lb_metric[3], "HealthyHostCount": lb_metric[4], "UnHealthyHostCount": lb_metric[5]}
    print(json.dumps(stats))
except:
    raise
