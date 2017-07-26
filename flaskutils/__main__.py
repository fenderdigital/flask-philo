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
        root_folders = ('docker', 'documentation', 'src', 'tools')
        for folder in root_folders:
            os.mkdir('./' + project_name + '/{}'.format(folder))

        open('./' + project_name + '/README.md', 'x')

        create_from_template(**{
            "project_name": project_name,
            "path": "",
            "filename": "Vagrantfile",
        })

        # ./docker
        os.mkdir('./' + project_name + '/docker/development')

        docker_files = (
            'Dockerfile',
            'Dockerfile_postgres',
            'docker-compose.yml',
            'wait-for-it.sh'
        )
        for dfile in docker_files:
            create_from_template(**{
                "project_name": project_name,
                "path": "docker/development",
                "filename": dfile,
            })

        # ./src
        src_folders = (
            'app', 'bdd_tests', 'config', 'console_commands', 'tests')
        for folder in src_folders:
            os.mkdir('./' + project_name + '/src/{}'.format(folder))

        src_files = ('manage.py', 'run_bdd_tests.py')
        for sfile in src_files:
            create_from_template(**{
                "project_name": project_name,
                "path": "src",
                "filename": sfile,
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

        # ./src/bdd_tests
        create_from_template(**{
            "project_name": project_name,
            "path": "src/bdd_tests",
            "filename": "environment.py",
        })

        bdd_folders = ('config', 'features', 'page_objects', 'steps')
        for folder in bdd_folders:
            os.mkdir('./' + project_name + '/src/bdd_tests/{}'.format(folder))
            open(
                './' + project_name + '/src/bdd_tests/{}/__init__.py'.format(
                    folder), 'x')

        create_from_template(**{
            "project_name": project_name,
            "path": "src/bdd_tests/config",
            "filename": "local_settings.py",
        })

        create_from_template(**{
            "project_name": project_name,
            "path": "src/bdd_tests/features",
            "filename": "example.feature",
        })

        create_from_template(**{
            "project_name": project_name,
            "path": "src/bdd_tests/steps",
            "filename": "example_steps.py",
        })

        # ./src/config
        config_files = ('development.py', 'test.py', 'docker_development.py')
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
        tools_folders = ('requirements', 'provision')
        for folder in tools_folders:
            os.mkdir('./' + project_name + '/tools/{}'.format(folder))

        req_files = ('dev.txt', 'base.txt')
        for rfile in req_files:
            create_from_template(**{
                "project_name": project_name,
                "path": "tools/requirements",
                "filename": rfile,
            })

        prov_files = (
            'bootstrap.sh', 'install_postgresql.sh', 'install_python.sh')
        for pfile in prov_files:
            create_from_template(**{
                "project_name": project_name,
                "path": "tools/provision",
                "filename": pfile,
            })


if __name__ == "__main__":
    main()
