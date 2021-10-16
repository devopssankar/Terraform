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
parser.add_option("-b", "--bucket", dest="bucketname",
                                help="BucketName")
(options, args) = parser.parse_args()

if (options.profile == None):
    parser.error("-a aws account name is required")


boto3.setup_default_session(profile_name=options.profile)


# Get Bucket StandardStorage Size
if (options.bucketname != None):
  size_dict = {}
  end = datetime.datetime.utcnow()
  start = datetime.datetime.now() - datetime.timedelta(days = 2)
  cw = boto3.client('cloudwatch', options.region)
  res = cw.get_metric_statistics(Namespace='AWS/S3', MetricName='BucketSizeBytes', StartTime=start, EndTime=end, Period=86400, Statistics=["Average"], Dimensions=[{'Name': "StorageType", 'Value': "StandardStorage"}, {'Name': "BucketName", 'Value': options.bucketname}])
  datapoints = res.get('Datapoints')
  if len(datapoints) != 0:
      average = datapoints[-1].get('Average')
  else:
      average = 0
  print("%i" % average)
# Populate StandardStorage Cost data when needed (comment above line and uncomment below three lines)
#  cost = (average/1000**3.0)*0.023
#  costsize= {"Size": round(average), "Cost": round(cost)}
#  print(json.dumps(costsize))

# Buckets Discovery
else:
  bucket_dict = {}
  bucket_list = []
  s3 = boto3.client('s3')
  if (options.region != "us-east-1"):
      for bucket in s3.list_buckets()['Buckets']:
          if s3.get_bucket_location(Bucket=bucket['Name'])['LocationConstraint'] == options.region:
              bucket_name_dict = { "{#BUCKET}": bucket['Name'] }
              bucket_list.append(bucket_name_dict)
              bucket_dict['data'] = bucket_list
      print(json.dumps(bucket_dict))
  else:
      for bucket in s3.list_buckets()['Buckets']:
          if s3.get_bucket_location(Bucket=bucket['Name'])['LocationConstraint'] == None:
              bucket_name_dict = { "{#BUCKET}": bucket['Name'] }
              bucket_list.append(bucket_name_dict)
              bucket_dict['data'] = bucket_list
      print(json.dumps(bucket_dict))
