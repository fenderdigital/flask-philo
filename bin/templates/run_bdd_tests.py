from rfqa.bdd.runner import run_bdd

import argparse
import os
import time

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_DIR = os.path.join(BASE_DIR, 'bdd_tests')


def main():
    description = 'Run bdd tests'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '--settings', help='config file path',
        default='bdd_tests.config.local_settings')

    parser.add_argument('--tags', required=False)

    args, extra_params = parser.parse_known_args()

    kwargs = {}
    if args.tags:
        kwargs['--tags'] = args.tags

    os.environ.setdefault('BDDRF_SETTINGS_MODULE', args.settings)
    os.environ.setdefault('PLAYWEB_SRC_DIR', BASE_DIR)

    run_bdd(TEST_DIR, **kwargs)

    time.sleep(2)


if __name__ == '__main__':
    main()
