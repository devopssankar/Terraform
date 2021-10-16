#!/usr/bin/env python3

import boto3
import argparse
import time
import csv

def get_options():
  parser = argparse.ArgumentParser()
  parser.add_argument('-p','--profile', metavar='profile', help='profile in .aws/config', required=False)
  args = vars(parser.parse_args())
  profile = args['profile']
  return(profile)


def write_csv(name, list_bukets):
    timestr = time.strftime("_%Y%m%d.csv")
    filename = name + timestr
    with open(filename, 'a+') as csv_file:
        writer = csv.writer(csv_file)
        for row in list_bukets:
            writer.writerow(row)


def connect_s3(profile):
    if(profile != None):
        boto3.setup_default_session(profile_name=profile)
    resource = boto3.resource('s3')
    client = boto3.client('s3')
    return(resource, client)


def check_bucket(bucket, client):
    try:
        bucket_location = client.get_bucket_location(Bucket=bucket)['LocationConstraint']
    except:
        return(bucket, "FAIL_LOC", "FAIL", "FAIL")
    try:
        bucket_acl = client.get_bucket_acl(Bucket=bucket)
    except:
        return(bucket, "FAIL", "FAIL_ACL", "FAIL_ACL")

    permission = []
    auth_permission = []
    AllUsers = []
    AuthUsers = []

    for grants in bucket_acl['Grants']:
        if ('URI' in grants['Grantee']) and ('AllUser' in grants['Grantee']['URI']):
            permission.append(grants['Permission'])
        if ('URI' in grants['Grantee']) and ('AuthenticatedUsers' in grants['Grantee']['URI']):
            auth_permission.append(grants['Permission'])

    for perm in permission:
        AllUsers.append(perm)

    for auth_perm in auth_permission:
        AuthUsers.append(auth_perm)

    return(bucket, bucket_location, AllUsers, AuthUsers)



def s3_perm_chk(profile):
    resource, client = connect_s3(profile)
    data = []
    header = ['Name', 'Region', 'AllUsers Permission', 'AuthUsers Permission', 'Encrypted', 'DataClassification', 'Costcentre', 'ApplicationName']
    data.append(header)
    for bucket in resource.buckets.all():
        bucket, bucket_location, AllUsers, AuthUsers =  check_bucket(bucket.name, client)
        row = []
        row.append(bucket)
        row.append(bucket_location if bucket_location != None else 'us-east-1')
        row.append(AllUsers if len (AllUsers) > 0 else 'None')
        row.append(AuthUsers if len (AuthUsers) > 0 else 'None')
        try:
            enc_response = client.get_bucket_encryption(Bucket=bucket)
            row.append (enc_response['ServerSideEncryptionConfiguration']['Rules'][0]['ApplyServerSideEncryptionByDefault']['SSEAlgorithm'])
        except Exception as err:
            row.append('No')
        try:
            tag_response = client.get_bucket_tagging(Bucket=bucket)
            DataClassification = 'No'
            CostCenter = 'No'
            ApplicationName = 'No'
            for TagSet in tag_response['TagSet']:
                if 'DataClassification' in TagSet['Key']:
                    DataClassification = TagSet['Value']
                if 'CostCenter' in TagSet['Key']:
                    CostCenter = TagSet['Value']
                if 'ApplicationName' in TagSet['Key']:
                    ApplicationName = TagSet['Value']
            row.append(DataClassification)
            row.append(CostCenter)
            row.append(ApplicationName)
        except Exception as err:
            row.append('No')
            row.append('No')
            row.append('No')
        data.append (row)
    write_csv("s3_access_report", data)


def connect_bucket(bucket, client):
    data = []
    try:
        bucket_acl = client.get_bucket_acl(Bucket=bucket)
    except:
        return [(bucket, "FAIL", "FAIL_ACL", "FAIL_ACL")]
    for grants in bucket_acl['Grants']:
        auth_user_response = grants['Grantee']
        if 'DisplayName' in auth_user_response:
            displayname = auth_user_response['DisplayName']
        elif 'ID' in auth_user_response:
            displayname = auth_user_response['ID']
        else:
            displayname = auth_user_response['URI']
        permission = grants['Permission']
        data.append([bucket, displayname, permission])
    return data


def s3_auth_users(profile):
    resource, client = connect_s3(profile)
    data = []
    title = ['Name', 'DisplayName', 'Permission']
    data.append(title)
    for bucket in resource.buckets.all():
        for record in connect_bucket(bucket.name, client):
            data.append (record)
    write_csv("s3_authuers_report", data)


def s3_life_cycle(profile):
    resource, client = connect_s3(profile)
    data = []
    header = ['BucketName', 'Policy', 'Name', 'Status', 'Expiration']
    data.append(header)
    bucket_list = client.list_buckets()
    for bucket in bucket_list['Buckets']:
        row = []
        row.append(bucket['Name'])
        try:
            lifecycle = client.get_bucket_lifecycle(Bucket=bucket['Name'])
            if "Rules" in lifecycle:
                row.append('Yes')
            rules = lifecycle['Rules']
            for record in rules:
                if "Expiration" in record:
                    row.append(record['ID'])
                    row.append(record['Status'])
                    row.append(record['Expiration']['Days'])
        except:
            row.append('No')
        data.append(row)
    write_csv("s3_lifecycle_report", data)


if __name__ == "__main__":
    try:
        profile = get_options()
        s3_perm_chk(profile)
        s3_auth_users(profile)
        s3_life_cycle(profile)
    except Exception as err:
        print(err)
