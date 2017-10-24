import argparse
import os
import pytest


def run(**kwargs):
    app = kwargs['app']
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--q', help='test file path', required=False,
        default=os.path.join(app.config['BASE_DIR'], 'tests'))
    parser.add_argument(
        '--x', help='regex for tests to be run', required=False,
        default='test_')
    args, extra_params = parser.parse_known_args()
    exit(pytest.main(['-s', args.q, '-k', args.x]))
