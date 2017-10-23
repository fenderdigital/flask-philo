import argparse
import os

from . import (
    cloudformation, key_pair, sqs
)


def run(**kwargs):
    valid_commands = {
        'sqs': sqs, 'cloudformation': cloudformation, 'key_pair': key_pair
    }

    description = 'AWS Flaskutils'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('command', help='command to execute')
    parser.add_argument('aws_subcommand', help='aws command to execute')
    parser.add_argument('action', help='aws  action')
    arg, extra_params = parser.parse_known_args()
    if arg.aws_subcommand not in valid_commands:
        print('\n{} is not a valid command\n'.format(arg.aws_subcommand))
        print('Valid commands are:\n')
        for cm in valid_commands:
            print('* {} \n'.format(cm))
        exit(1)
    #os.environ.setdefault('FLASKUTILS_SETTINGS_MODULE', args.settings)
    app = kwargs['app']
    if 'credentials' in app.config.get('AWS', {}):
        cred = app.config['AWS']['credentials']['aws_access_key_id']
        os.environ['AWS_ACCESS_KEY_ID'] = cred
        cred = app.config['AWS']['credentials']['aws_secret_access_key']
        os.environ['AWS_SECRET_ACCESS_KEY'] = cred

    if ('AWS_SECRET_ACCESS_KEY' not in os.environ
            or 'AWS_ACCESS_KEY_ID' not in os.environ):
        print('Invalid AWS credentials\n')
        exit(1)
    valid_commands[arg.aws_subcommand].run(app, arg.action)
