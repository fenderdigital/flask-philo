import argparse
import os
import pytest


def run(**kwargs):
    app = kwargs['app']
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--q', help='config file path', required=False,
        default=os.path.join(app.config['BASE_DIR'], 'tests'))
    args, extra_params = parser.parse_known_args()
    exit(pytest.main(['-s', args.q]))
