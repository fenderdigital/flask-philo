from setuptools import setup

setup(
    name='flaskutils',
    version='1.2.0',
    description='Flask Utilities',
    packages=['flaskutils', 'flaskutils.commands_flaskutils'],
    author='Manuel Ignacio Franco Galeano',
    author_email='maigfrga@gmail.com',
    install_requires=[
        'jsonschema',
        'pytest',
        'flask',
        'flask_oauthlib'
    ],
)
