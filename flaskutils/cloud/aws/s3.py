from .utils import run_action
from prettytable import PrettyTable


import argparse
import boto3
import boto3.ec2
import os


app = None


def download_file(fname, bucket, key, region=None):
    client = boto3.client('s3', region_name=region)
    return client.download_file(
        bucket, key, fname)


def upload_file(fname, bucket, key, region=None):
    client = boto3.client('s3', region_name=region)
    return client.upload_file(fname, bucket, key)


def upload_dir(root_folder, bucket, region=None):
    client = boto3.client('s3', region_name=region)

    # remove backslash
    if root_folder.endswith('/'):
        root_folder = root_folder[:-1]

    for root, dirs, files in os.walk(root_folder):
        for name in files:
            fname = os.path.join(root, name)
            app.logger.info(
                'uploading file {} to bucket {}'.format(fname, bucket))
            client.upload_file(fname, bucket, fname)


def list_objects_v2(bucket, region):
    client = boto3.client('s3', region_name=region)
    return client.list_objects_v2(Bucket=bucket)


def run(dapp, cmd):
    global app
    app = dapp

    def list_objects_v2_cmd():
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--region', required=True, help='AWS Region')
        parser.add_argument(
            '--bucket', required=True, help='S3 Bucket Name'
        )

        args, extra_params = parser.parse_known_args()

        t = PrettyTable([
               '', 'Key', 'Last Modified', 'Size (bytes) ', 'Storage Class'

        ])

        index = 1
        data = list_objects_v2(args.bucket, args.region)
        if 'Contents' in data:
            for item in data['Contents']:
                t.add_row([
                    index, item['Key'], item['LastModified'], item['Size'],
                    item['StorageClass']
                ])
                index += 1
        print(t)

    def upload_file_cmd():
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--region', required=True, help='AWS Region')
        parser.add_argument(
            '--bucket', required=True, help='S3 Bucket Name'
        )
        parser.add_argument(
            '--fname', required=True, help='File to upload'
        )
        parser.add_argument(
            '--key', required=True, help='File to upload Key'
        )
        args, extra_params = parser.parse_known_args()
        upload_file(args.fname, args.bucket, args.key, region=args.region)

    def download_file_cmd():
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--region', required=True, help='AWS Region')
        parser.add_argument(
            '--bucket', required=True, help='S3 Bucket Name'
        )
        parser.add_argument(
            '--fname', required=True, help='File to upload'
        )
        parser.add_argument(
            '--key', required=True, help='File to upload Key'
        )
        args, extra_params = parser.parse_known_args()
        download_file(args.fname, args.bucket, args.key, region=args.region)

    def upload_dir_cmd():
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--region', required=True, help='AWS Region')
        parser.add_argument(
            '--bucket', required=True, help='S3 Bucket Name'
        )
        parser.add_argument(
            '--dir_name', required=True, help='Directory to upload'
        )
        args, extra_params = parser.parse_known_args()
        upload_dir(args.dir_name, args.bucket, region=args.region)

    actions = {
        'list_objects_v2': list_objects_v2_cmd,
        'upload_file': upload_file_cmd,
        'download_file': download_file_cmd,
        'upload_dir': upload_dir_cmd
    }

    run_action(actions, cmd)
