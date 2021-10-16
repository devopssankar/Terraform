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
parser.add_option("-f", "--FsId", dest="FsId",
                help="Elastic File System Id")

(options, args) = parser.parse_args()

if (options.profile == None):
    parser.error("-a aws account name is required")
if (options.FsId == None):
    parser.error("-f elastic filesystem id is required")

boto3.setup_default_session(profile_name=options.profile)
client = boto3.client('efs', options.region)
res = client.describe_file_systems(FileSystemId=options.FsId)
state = res['FileSystems'][0]['LifeCycleState']
mount = res['FileSystems'][0]['NumberOfMountTargets']
size = res['FileSystems'][0]['SizeInBytes']['Value']
pmode = res['FileSystems'][0]['PerformanceMode']
tmode = res['FileSystems'][0]['ThroughputMode']
enc = res['FileSystems'][0]['Encrypted']
stats = {"LifeCycleState": state, "NumberOfMountTargets": mount, "SizeInBytes": size, "PerformanceMode": pmode, "ThroughputMode": tmode, "Encrypted": enc}
print(json.dumps(stats))
