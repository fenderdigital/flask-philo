from .utils import run_action
from prettytable import PrettyTable


import argparse
import boto3
import boto3.ec2
import os


app = None


def create_key_pair(key_name, key_dir='~/.ssh', region=None):
    client = boto3.client('ec2', region_name=region)
    key = client.create_key_pair(KeyName=key_name)

    if 'KeyMaterial' not in key:
        print('Key could not be created\n')
        raise
    else:
        fname = os.path.join(key_dir, '{}.pem'.format(key_name))

        with open(fname, 'w') as f:
            f.write(key['KeyMaterial'])
    return key


def describe_key_pairs():
    """
    Returns all key pairs for region
    """
    region_keys = {}
    for r in boto3.client('ec2', 'us-west-2').describe_regions()['Regions']:
        region = r['RegionName']
        client = boto3.client('ec2', region_name=region)
        try:
            pairs = client.describe_key_pairs()
            if pairs:
                region_keys[region] = pairs
        except Exception as e:
            app.logger.info(e)
    return region_keys


def run(dapp, cmd):
    global app
    app = dapp

    def cmd_describe_key_pairs():
        t = PrettyTable([
                'KeyName', 'KeyFingerprint', 'Region'

        ])
        for region, keys in describe_key_pairs().items():
            for pair in keys['KeyPairs']:
                t.add_row([pair['KeyName'], pair['KeyFingerprint'], region])

        print(t)

    def cmd_create_key_pair():
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--region', required=True, help='AWS Region')
        parser.add_argument('--key_name', required=True)
        parser.add_argument(
            '--key_dir', required=False, default='~/.ssh',
            help='Directory where key will be stored')

        args, extra_params = parser.parse_known_args()
        pair = create_key_pair(
            args.key_name, key_dir=args.key_dir, region=args.region)
        t = PrettyTable([
                'KeyName', 'KeyFingerprint', 'Region'

        ])
        t.add_row([pair['KeyName'], pair['KeyFingerprint'], args.region])
        print(t)

    actions = {
        'create_key_pair': cmd_create_key_pair,
        'describe_key_pairs': cmd_describe_key_pairs,
    }
    run_action(actions, cmd)
