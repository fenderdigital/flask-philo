from setuptools import setup

setup(
    name='flaskutils',
    version='2.0.0',
    description='Flask Utilities',
    packages=[
        'flaskutils', 'flaskutils.commands_flaskutils', 'flaskutils.db',
        'flaskutils.db.postgresql'],
    author='Manuel Ignacio Franco Galeano',
    author_email='maigfrga@gmail.com',
    install_requires=[
        'jsonschema',
        'pytest',
        'flask',
        'flask_oauthlib',
        'bcrypt',
        'SQLAlchemy>=1.0'
    ],
)
