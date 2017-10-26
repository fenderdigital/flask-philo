from setuptools import setup


setup(
    name='Flask-Philo',
    version='3.0.0',
    description='Simple web framework based on Flask',
    packages=[
        'flask_philo', 'flask_philo.commands_flask_philo', 'flask_philo.db',
        'flask_philo.db.postgresql', 'flask_philo.db.redis',
        'flask_philo.db.elasticsearch', 'flask_philo.cloud',
        'flask_philo.cloud.aws', 'flask_philo.templates'
        ],
    package_data={
        'flask_philo.templates': '*'
    },
    author='Manuel Ignacio Franco Galeano',
    author_email='maigfrga@gmail.com',
    install_requires=[
        'psycopg2',
        'jsonschema',
        'pytest',
        'flask',
        'flask_oauthlib',
        'bcrypt',
        'SQLAlchemy',
        'redis',
        'elasticsearch',
        'boto3',
        'PrettyTable'
    ],
    entry_points={
        "console_scripts": [
            "flask-philo-admin = flask_philo.admin:main",
        ]
    }
)
