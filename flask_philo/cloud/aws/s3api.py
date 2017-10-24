from .utils import run_action
from prettytable import PrettyTable


import argparse
import boto3
import boto3.ec2


app = None


def create_bucket(bucket=None, location_constraint=None):
    client = boto3.client('s3')
    create_bucket_configuration = {}
    if location_constraint:
        create_bucket_configuration["LocationConstraint"] =\
            location_constraint
    return client.create_bucket(
        Bucket=bucket,
        CreateBucketConfiguration=create_bucket_configuration,
    )


def delete_bucket(bucket=None):
    client = boto3.client('s3')
    return client.delete_bucket(Bucket=bucket)


def list_buckets():
    result = []
    client = boto3.client('s3')
    bucket_list = client.list_buckets()
    if 'Buckets' in bucket_list:
        for b in bucket_list['Buckets']:
            b['location'] = client.get_bucket_location(
                Bucket=b['Name'])['LocationConstraint']
            result.append(b)
    return result


def run(dapp, cmd):
    global app
    app = dapp

    def create_bucket_cmd():
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--region', required=False, help='AWS Region')
        parser.add_argument(
            '--bucket', required=True, help='S3 Bucket Name'
        )

        args, extra_params = parser.parse_known_args()

        print(create_bucket(
            location_constraint=args.region, bucket=args.bucket))

    def list_buckets_cmd():
        t = PrettyTable([
               '', 'Name', 'Creation Date', 'Location'

        ])
        index = 1
        for q in list_buckets():
            t.add_row([index, q['Name'], q['CreationDate'], q['location']])
            index += 1
        print(t)

    def delete_bucket_cmd():
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--bucket', required=True, help='S3 Bucket Name'
        )

        args, extra_params = parser.parse_known_args()

        print(delete_bucket(bucket=args.bucket))

    actions = {
        'list_buckets': list_buckets_cmd,
        'create_bucket': create_bucket_cmd,
        'delete_bucket': delete_bucket_cmd
    }
    run_action(actions, cmd)
