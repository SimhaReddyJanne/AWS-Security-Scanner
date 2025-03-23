import boto3
import json
import csv

# Initialize AWS Clients
iam_client = boto3.client('iam')
s3_client = boto3.client('s3')

# Data storage
scan_results = {
    "iam_users": [],
    "iam_users_without_mfa": [],
    "s3_buckets": [],
    "public_s3_buckets": []
}

# Function to list IAM Users
def list_iam_users():
    users = iam_client.list_users()['Users']
    for user in users:
        username = user['UserName']
        scan_results["iam_users"].append({"username": username})

# Function to check IAM Users without MFA
def check_iam_mfa():
    users = iam_client.list_users()['Users']
    for user in users:
        username = user['UserName']
        mfa_devices = iam_client.list_mfa_devices(UserName=username)
        if not mfa_devices['MFADevices']:
            scan_results["iam_users_without_mfa"].append({"username": username})

# Function to list S3 Buckets
def list_s3_buckets():
    buckets = s3_client.list_buckets()['Buckets']
    for bucket in buckets:
        bucket_name = bucket['Name']
        scan_results["s3_buckets"].append({"bucket_name": bucket_name})

# Function to check public S3 Buckets
def check_public_s3_buckets():
    buckets = s3_client.list_buckets()['Buckets']
    for bucket in buckets:
        bucket_name = bucket['Name']
        acl = s3_client.get_bucket_acl(Bucket=bucket_name)
        for grant in acl['Grants']:
            if 'URI' in grant['Grantee'] and "AllUsers" in grant['Grantee']['URI']:
                scan_results["public_s3_buckets"].append({"bucket_name": bucket_name})

# Lambda Handler
def lambda_handler(event, context):
    list_iam_users()
    check_iam_mfa()
    list_s3_buckets()
    check_public_s3_buckets()

    # Save to JSON
    json_results = json.dumps(scan_results, indent=4)
    print(json_results)

    # Upload results to S3 (optional)
    s3 = boto3.client('s3')
    bucket_name = "your-security-scanner-reports"
    file_name = "aws_security_scan_results.json"
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=json_results)

    return {
        "statusCode": 200,
        "body": json_results
    }
