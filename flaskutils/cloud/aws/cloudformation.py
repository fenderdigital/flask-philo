from .utils import parse_tags


import argparse
import boto3
import boto3.ec2


def create_stack(region, **params):
    client = boto3.client('cloudformation', region_name=region)

    if 'OnFailure' not in params:
        params['OnFailure'] = 'DELETE'
    return client.create_stack(**params)


def list_stacks(tags=None):
    region_stack = {}
    for r in boto3.client('ec2', 'us-west-2').describe_regions()['Regions']:
        region = r['RegionName']
        client = boto3.client('cloudformation', region_name=region)
        try:
            l = client.list_stacks()
            if l:
                region_stack[region] = l
        except Exception:
            pass

    return region_stack


def delete_stack(region, stack_name):
    client = boto3.client('cloudformation', region_name=region)
    return client.delete_stack(StackName=stack_name)


def update_stack(region, **params):
    client = boto3.client('cloudformation', region_name=region)
    return client.update_stack(**params)




def run(cmd):

    def cmd_create_stack():
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--region', required=True, help='AWS Region')
        parser.add_argument('--name', required=True)
        parser.add_argument(
            '--template', required=True, help='')
        parser.add_argument('--json_params', required=True)
        arg = parser.parse_args()

        params = {}

        with open(arg.template, 'r') as f:
            template = f.read()

        with open(arg.json_params, 'r') as f:
            params['Parameters'] = json.loads(f.read())
        params['StackName'] = args.name
        params['TemplateBody'] = template
        params['Tags'] = [{'Key': 'Name', 'Value': args.name}]
        print(create_stack(args.region, **params))


    def cmd_list_stacks():
        parser = argparse.ArgumentParser()
        parser.add_argument('--tags', required=False, nargs='+')
        arg = parser.parse_args()
        tags = parse_args(arg.tags)

        for k, v in list_stacks(tags=tags).items():
            print('Instances in region {}: \n'.format(k))
            if v['StackSummaries']:
                print(v['StackSummaries'])

    def cmd_delete_stack():
        pass

    def cmd_update_stack():
        pass

    actions = {
        'create_stack': cmd_create_stack,
        'list_stacks': cmd_list_stacks,
        'delete_stack': cmd_delete_stack,
        'update_stack': cmd_update_stack
    }

    actions[cmd]()
