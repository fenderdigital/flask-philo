from setuptools import setup


setup(
    name='Flask-Philo',
    version='3.5.2',
    description='Simple web framework based on Flask',
    long_description='Flask based framework to build RESTful microservices',
    packages=[
        'flask_philo', 'flask_philo.commands_flask_philo', 'flask_philo.db',
        'flask_philo.db.postgresql', 'flask_philo.db.redis',
        'flask_philo.db.elasticsearch', 'flask_philo.cloud',
        'flask_philo.cloud.aws', 'flask_philo.templates', 'flask_philo.jinja2'
        ],
    package_data={
        'flask_philo.templates': ['*']
    },
    url='https://github.com/Riffstation/flask-philo',
    author='Manuel Ignacio Franco Galeano',
    author_email='maigfrga@gmail.com',
    license='Apache',
    install_requires=[
        'psycopg2',
        'jsonschema',
        'pytest',
        'Flask',
        'flask_oauthlib',
        'bcrypt',
        'SQLAlchemy',
        'redis',
        'elasticsearch',
        'boto3',
        'PrettyTable',
        'jinja2==2.10'
    ],
    python_requires='>=3',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Framework :: Flask',
        'Programming Language :: Python :: 3',
    ],
    keywords='web framework flask microservice',
    entry_points={
        "console_scripts": [
            "flask-philo-admin = flask_philo.admin:main",
        ]
    }
)
