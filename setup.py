from setuptools import setup


setup(
    name='flaskutils',
    version='2.7.1',
    description='Flask Utilities',
    packages=[
        'flaskutils', 'flaskutils.commands_flaskutils', 'flaskutils.db',
        'flaskutils.db.postgresql', 'flaskutils.db.redis',
        'flaskutils.db.elasticsearch', 'flaskutils.cloud',
        'flaskutils.cloud.aws'
        ],
    author='Manuel Ignacio Franco Galeano',
    author_email='maigfrga@gmail.com',
    install_requires=[
        'psycopg2',
        'jsonschema',
        'pytest',
        'flask',
        'flask_oauthlib',
        'bcrypt',
        'SQLAlchemy>=1.0',
        'redis',
        'elasticsearch',
        'boto3',
        'PrettyTable'
    ],
    entry_points={
        "console_scripts": [
            "flaskutils-admin = flaskutils.__main__:main",
        ]
    }
)
