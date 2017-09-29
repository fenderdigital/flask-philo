import os
import argparse
import pkg_resources
from jinja2 import Template


def create_from_template(**data):
    resource_package = __name__  # Could be any module/package name
    template_folder = '../bin/templates/'
    project_name = data['project_name']
    path = data['path']
    filename = data['filename']

    resource_path = template_folder + filename
    template = pkg_resources.resource_stream(resource_package, resource_path)

    with open(template.name, 'r') as f:
        params = {
            "project_name": project_name
        }
        t = Template(f.read())
        template = t.render(**params)

    with open('./{}/{}/{}'.format(project_name, path, filename), 'w') as f:
        f.write(template)
        if template:
            f.write("\n")


def main():
    parser = argparse.ArgumentParser(
        description='admin tool for flaskutils projects')
    parser.add_argument('command', help='command to be executed')
    parser.add_argument('name', help='name of project')

    args = parser.parse_args()
    if ('command' in vars(args) and args.command == 'startproject'):
        # ./
        project_name = args.name
        os.mkdir('./' + project_name)
        root_folders = ('documentation', 'src', 'tools')
        for folder in root_folders:
            os.mkdir('./' + project_name + '/{}'.format(folder))

        open('./' + project_name + '/README.md', 'x')

        # ./src
        src_folders = (
            'app', 'config', 'console_commands', 'tests')
        for folder in src_folders:
            os.mkdir('./' + project_name + '/src/{}'.format(folder))

        create_from_template(**{
            "project_name": project_name,
            "path": "src",
            "filename": "manage.py",
        })

        # ./src/app
        app_folders = ('models', 'serializers', 'views')
        for folder in app_folders:
            os.mkdir('./' + project_name + '/src/app/{}'.format(folder))
            open('./' + project_name + '/src/app/{}/__init__.py'.format(
                folder), 'x')

        open('./' + project_name + '/src/app/__init__.py', 'x')

        create_from_template(**{
            "project_name": project_name,
            "path": "src/app",
            "filename": "urls.py",
        })

        create_from_template(**{
            "project_name": project_name,
            "path": "src/app/views",
            "filename": "example_views.py",
        })

        # ./src/config
        config_files = ('development.py', 'test.py')
        for cfile in config_files:
            create_from_template(**{
                "project_name": project_name,
                "path": "src/config",
                "filename": cfile,
            })

        # ./src/console_commands
        create_from_template(**{
            "project_name": project_name,
            "path": "src/console_commands",
            "filename": "__init__.py",
        })

        # ./src/tests
        open('./' + project_name + '/src/tests/__init__.py', 'x')

        create_from_template(**{
            "project_name": project_name,
            "path": "src/tests",
            "filename": "test_views.py",
        })

        # ./tools
        os.mkdir('./' + project_name + '/tools/requirements')

        req_files = ('dev.txt', 'base.txt')
        for rfile in req_files:
            create_from_template(**{
                "project_name": project_name,
                "path": "tools/requirements",
                "filename": rfile,
            })


if __name__ == "__main__":
    main()
