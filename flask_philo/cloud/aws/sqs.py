from .utils import run_action
from prettytable import PrettyTable


import argparse
import boto3
import boto3.ec2
import json
import uuid


app = None


def send_message(queue_url, message_body, region=None):
    client = boto3.client('sqs', region_name=region)
    return client.send_message(QueueUrl=queue_url, MessageBody=message_body)


def send_message_batch(queue_url, entries, region=None):
    client = boto3.client('sqs', region_name=region)
    return client.send_message_batch(
        QueueUrl=queue_url, Entries=entries)


def list_queues():
    region_queues = {}
    for r in boto3.client('ec2', 'us-west-2').describe_regions()['Regions']:
        region = r['RegionName']
        client = boto3.client('sqs', region_name=region)
        try:
            queues = client.list_queues()
            if queues:
                region_queues[region] = queues
        except Exception as e:
            app.logger.info(e)
    return region_queues


def create_queue(queue_name, region=None, attributes={}):
    client = boto3.client('sqs', region_name=region)
    return client.create_queue(QueueName=queue_name, Attributes=attributes)


def receive_message(queue_url, max_number_of_messages=1, region=None):
    client = boto3.client('sqs', region_name=region)
    result = client.receive_message(
        QueueUrl=queue_url, MaxNumberOfMessages=max_number_of_messages)
    return result


def delete_message(queue_url, receipt_handle, region=None):
    client = boto3.client('sqs', region_name=region)
    result = client.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )
    return result


def purge_queue(queue_url, region=None):
    client = boto3.client('sqs', region_name=region)
    result = client.purge_queue(
        QueueUrl=queue_url,
    )
    return result


def delete_queue(queue_url, region=None):
    client = boto3.client('sqs', region_name=region)
    result = client.delete_queue(
        QueueUrl=queue_url,
    )
    return result


def run(dapp, cmd):
    global app
    app = dapp

    def list_queues_cmd():
        t = PrettyTable([
                'Queue Url', 'Region'

        ])
        for region, data in list_queues().items():
            if 'QueueUrls' in data:
                for q in data['QueueUrls']:
                    t.add_row([q, region])
        print(t)

    def send_message_batch_cmd():
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--region', required=True, help='AWS Region')
        parser.add_argument('--queue_url', required=True)
        parser.add_argument('--entries', required=True)
        args, extra_params = parser.parse_known_args()
        entries = [
            {'Id': str(uuid.uuid4()), 'MessageBody': str(entry)}
            for entry in json.loads(args.entries)]

        print(
            send_message_batch(
                args.queue_url, entries, region=args.region))

    def send_message_cmd():
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--region', required=True, help='AWS Region')
        parser.add_argument('--queue_url', required=True)
        parser.add_argument('--message_body', required=True)
        args, extra_params = parser.parse_known_args()
        print(
            send_message(
                args.queue_url, args.message_body, region=args.region))

    def create_queue_cmd():
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--region', required=True, help='AWS Region')
        parser.add_argument('--queue_name', required=True)
        parser.add_argument('--json_attributes', required=False, default='{}')
        args, extra_params = parser.parse_known_args()
        print(
            create_queue(
                args.queue_name, region=args.region,
                attributes=json.loads(args.json_attributes)))

    def receive_message_cmd():
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--region', required=True, help='AWS Region')
        parser.add_argument('--queue_url', required=True)
        parser.add_argument(
            '--max_number_of_messages', required=False, default=1, type=int)
        args, extra_params = parser.parse_known_args()
        print(
            receive_message(
                args.queue_url,
                max_number_of_messages=args.max_number_of_messages,
                region=args.region))

    def delete_message_cmd():
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--region', required=True, help='AWS Region')
        parser.add_argument('--queue_url', required=True)
        parser.add_argument('--receipt_handle', required=True)
        args, extra_params = parser.parse_known_args()
        print(
            delete_message(
                args.queue_url, args.receipt_handle, region=args.region)
        )

    def purge_queue_cmd():
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--region', required=True, help='AWS Region')
        parser.add_argument('--queue_url', required=True)
        args, extra_params = parser.parse_known_args()
        print(purge_queue(args.queue_url, region=args.region))

    def delete_queue_cmd():
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--region', required=True, help='AWS Region')
        parser.add_argument('--queue_url', required=True)
        args, extra_params = parser.parse_known_args()
        print(delete_queue(args.queue_url, region=args.region))

    actions = {
        'create_queue': create_queue_cmd,
        'list_queues': list_queues_cmd,
        'send_message': send_message_cmd,
        'send_message_batch': send_message_batch_cmd,
        'receive_message': receive_message_cmd,
        'delete_message': delete_message_cmd,
        'purge_queue': purge_queue_cmd,
        'delete_queue': delete_queue_cmd
    }

    run_action(actions, cmd)
