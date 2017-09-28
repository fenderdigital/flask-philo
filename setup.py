from setuptools import setup


setup(
    name='flaskutils',
    version='2.7.1',
    description='Flask Utilities',
    packages=[
        'flaskutils', 'flaskutils.commands_flaskutils', 'flaskutils.db',
        'flaskutils.db.postgresql', 'flaskutils.db.redis',
        'flaskutils.db.elasticsearch'],
    include_package_data=True,
    package_data = {
        '': ['../bin/templates/*']
    },
    author='Manuel Ignacio Franco Galeano',
    author_email='maigfrga@gmail.com',
    install_requires=[
        'jsonschema',
        'pytest',
        'flask',
        'flask_oauthlib',
        'bcrypt',
        'SQLAlchemy>=1.0',
        'redis',
        'elasticsearch'
    ],
    entry_points={
        "console_scripts": [
            "flaskutils-admin = flaskutils.__main__:main",
        ]
    }
)
