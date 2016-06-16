import argparse
import os
import pytest
import sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.join(BASE_DIR, '../'))


def run_tests():
    from flaskutils import init_app
    description = 'Creates play admin user'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '--settings', help='config file path', default='config.development')
    args = parser.parse_args()

    os.environ.setdefault('FLASKUTILS_SETTINGS_MODULE', args.settings)

    init_app(__name__)

    pytest.main(['-s'])


def main():
    run_tests()

if __name__ == '__main__':
    main()
