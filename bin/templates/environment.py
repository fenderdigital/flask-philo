from rfqa import conf
from playriffstation.http_client import InternalClient
from rfqa.reports import initialize_context_data, collect_data, generate_report
from rfqa.docker.utils import clean_docker
import os
import subprocess
import time


SSH_FILE = "id_rsa_github"

ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID", None)

SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", None)


def install_private_key():
    import boto3

    s3 = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY
    )

    try:
        os.stat(os.path.join("./.private_ssh_file/", SSH_FILE))
    except:
        os.mkdir("./.private_ssh_file")

    with open(os.path.join("./.private_ssh_file/", SSH_FILE), "wb") as data:
        s3.download_fileobj(
            conf.BUCKET,
            ".private_ssh_file/{}".format(SSH_FILE),
            data
        )


def run_docker():
    install_private_key()
    BASE_DIR = os.environ['PLAYWEB_SRC_DIR']
    env = conf.QA_ENVIRONMENT
    docker_dir = os.path.join(BASE_DIR, '../docker', env)
    cmd = [
        'sudo', 'docker-compose', 'build', '--no-cache'
    ]
    subprocess.check_output(cmd, cwd=docker_dir)
    cmd = [
        'sudo', 'docker-compose', 'stop'
    ]
    subprocess.check_output(cmd, cwd=docker_dir)
    cmd = [
        'sudo', 'docker-compose', 'up', '-d'
    ]
    subprocess.check_output(cmd, cwd=docker_dir)


def before_all(context):
    # set context vars here
    context.username = conf.USERNAME
    context.password = conf.PASSWORD
    context.client = InternalClient(context.username, context.password)
    context.example_url = conf.EXAMPLE_ENDPOINT

    clean_docker(clean_registry=False)
    run_docker()

    counter = 0
    while (counter < 20):
        print(
            "Awaiting client DB connection, attempt ",
            counter + 1, " of 20")
        try:
            result = context.client.get(context.example_url)
            if result.status == 200:
                print("OK status received")
                break
        except Exception as e:
            print("exception : ", e)

        counter = counter + 1
        time.sleep(5)

    initialize_context_data(context)


def before_scenario(context, scenario):
    if hasattr(context, 'response'):
        delattr(context, 'response')

    if hasattr(context, 'entity_id'):
        delattr(context, 'entity_id')


def after_scenario(context, scenario):
    if hasattr(context, 'response'):
        delattr(context, 'response')

    if hasattr(context, 'entity_id'):
        delattr(context, 'entity_id')


def after_feature(context, feature):
    context.features.append(context.feature)
    collect_data(context)


def after_all(context):
    generate_report(context.features, context.test_data)
