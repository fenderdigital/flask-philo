import os
import argparse
from jinja2 import Template

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


def create_from_template(**data):
    template_folder = os.path.join(BASE_DIR, 'templates')
    project_name = data['project_name']
    path = data['path']
    filename = data['filename']
    resource_path = os.path.join(template_folder, filename)

    with open(resource_path, 'r') as f:
        params = {
            'project_name': project_name
        }
        t = Template(f.read())
        template = t.render(**params)

    with open(os.path.join(path, filename), 'w') as f:
        f.write(template)
        if template:
            f.write('\n')


def start_project():
    parser = argparse.ArgumentParser(
        description='Admin tool for Flask-Philo projects')
    parser.add_argument('command', help='command to be executed')
    parser.add_argument('name', help='name of project')
    args = parser.parse_args()

    project_name = args.name

    dir_name = os.path.join(os.getcwd(), project_name)

    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    else:
        print('Directory {} already exists\n'.format(dir_name))
        exit(1)

    root_folders = ('documentation', 'src')
    for folder in root_folders:
        os.mkdir(os.path.join(dir_name, folder))

    create_from_template(**{
        'project_name': project_name,
        'path': dir_name,
        'filename': 'README.md',
    })

    # ./src
    src_folders = (
        'app', 'config', 'console_commands', 'tests', 'tools')

    for folder in src_folders:
        os.mkdir(os.path.join(dir_name, 'src', folder))

    create_from_template(**{
        'project_name': project_name,
        'path': os.path.join(dir_name, 'src'),
        'filename': 'manage.py',
    })

    # ./src/app
    app_folders = ('models', 'serializers', 'views')
    for folder in app_folders:
        os.mkdir(os.path.join(dir_name, 'src', 'app', folder))
        f = open(
            os.path.join(dir_name, 'src', 'app', folder, '__init__.py'), 'x')
        f.close()

    f = open(os.path.join(dir_name, 'src', 'app', '__init__.py'), 'x')
    f.close()

    create_from_template(**{
        'project_name': project_name,
        'path': os.path.join(dir_name, 'src', 'app'),
        'filename': 'urls.py',
    })

    create_from_template(**{
        'project_name': project_name,
        'path': os.path.join(dir_name, 'src', 'app', 'views'),
        'filename': 'example_views.py',
    })

    # ./src/config
    config_files = ('development.py', 'test.py')
    for cfile in config_files:
        create_from_template(**{
            'project_name': project_name,
            'path': os.path.join(dir_name, 'src', 'config'),
            'filename': cfile,
        })

    # ./src/console_commands
    create_from_template(**{
        'project_name': project_name,
        'path': os.path.join(dir_name, 'src', 'console_commands'),
        'filename': '__init__.py',
    })

    # ./src/tests
    f = open(os.path.join(dir_name, 'src', 'tests', '__init__.py'), 'x')
    f.close()

    create_from_template(**{
        'project_name': project_name,
        'path': os.path.join(dir_name, 'src', 'tests'),
        'filename': 'test_views.py',
    })

    # ./src/tools
    os.mkdir(os.path.join(dir_name, 'src', 'tools', 'requirements'))

    req_files = ('dev.txt', 'base.txt')
    for rfile in req_files:
        create_from_template(**{
            'project_name': project_name,
            'path': os.path.join(
                dir_name, 'src', 'tools', 'requirements'),
            'filename': rfile,
        })


def main():
    cmd = {
        'startproject': start_project
    }

    parser = argparse.ArgumentParser(
        description='Admin tool for Flask-Philo projects')
    parser.add_argument('command', help='command to be executed')
    args, extra_params = parser.parse_known_args()

    if args.command not in cmd:
        print('Invalid command. Valid commands are:')

        for k in cmd.keys():
            print('\n * {}'.format(k))

        exit(1)

    cmd[args.command]()


if __name__ == '__main__':
    main()
