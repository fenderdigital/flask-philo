Jinja Integration
=======================

`Jinja2 <http://jinja.pocoo.org/>`_ is one of the most popular templating engines for Python, and is packaged with Flask. Flask-Philo provides a number of additional methods to facilitate common calls to the Jinja2 engine

* **init_jinja2()** - Method description here
* **get_manager()** - Creates an instance of Flask-Philo's TemplatesManage class, facilitating multiple template loaders
* **set_request()** - append a request object to an Environment's global objects
* **render()** - Method description here
* **get_autoescaping_params()** - fetch a custom set of AutoEscaping rules from the Flask-Philo configuration file
* **load_extensions_from_config()** - Method description here
* **init_filesystem_loader()** - Method description here
* **init_loader()** - Method description here

init_jinja2()
#############

Single initialisation function that uses Flask-Philo's app configuration file (``/src/config/development.py``) to bootstrap the following Jinja2 components:

* Filesystem Loader
* Template Loader
* Autoescaping
* Extensions

*config/development.py* :

::

    JINJA2_TEMPLATES = {
        'DEFAULT': {
            'LOADER': 'FileSystemLoader',
            'PARAMETERS': {
                'path': (
                    os.path.join(BASE_DIR, '../', '_templates'),
                ),
                'encoding': 'utf-8',
                'followlinks': False
            },
            'AUTOESCAPING': {
                'enabled_extensions': ('html', 'htm', 'xml'),
                'disabled_extensions': [],
                'default_for_string': True,
                'default': False
            },
            'EXTENSIONS': (
                'tests.test_app.templatetags.TestExtension',
            )
        }
    }

Example Python code :

::

    from flask_philo import app
    from flask import g

    init_jinja2(g, app)
    assert hasattr(app, 'jinja_env')
    assert hasattr(app, 'jinja_options')
    assert hasattr(app, 'jinja_loader')
    assert hasattr(app, 'jinja_environment')


get_manager
###########

Creates an instance of Flask-Philo's TemplatesManager class, facilitating multiple template loaders

``get_manager()``

Example Python calling code :

::

    from flask_philo.jinja2 import get_manager

    # instantiate manager, and render html from template
    manager = get_manager()
    env = manager.environments['DEFAULT']
    template = env.get_template('home.html')
    output_html = template.render()


set_request
###########

Jinja2 uses a central object called the template *Environment*. Instances of this class are used to store the configuration and
global objects, and are used to load templates from the file system or other locations.

To append a request object to an Environment's global objects, use the ``set_request()`` method

Example Python calling code :
::

    from flask_philo import app
    from flask_philo.jinja2 import get_manager

    manager = get_manager()
    ctx = app.test_request_context('/hello-template')
    manager.set_request(ctx.request)
    env = manager.environments['DEFAULT']


get_autoescaping_params
#################

Flask-Philo allows us to specify a custom set of AutoEscaping rules in our application's configuration file (e.g. ``/src/config/development.py``).
These AutoEscaping rules may then used as part of our Environment instance

*config/development.py* :

::

    JINJA2_TEMPLATES = {
        'DEFAULT': {
            'AUTOESCAPING': {
                'enabled_extensions': ('html', 'htm', 'xml'),
                'disabled_extensions': [],
                'default_for_string': True,
                'default': False
            }
        }
    }

Example Python code :

::

    from flask_philo.jinja2 import get_autoescaping_params

    params = get_autoescaping_params(**app.config)
    env = Environment(
        autoescape=select_autoescape(**params),
    )


load_extensions_from_config
###########################

Flask-Philo allows us to specify a custom set of Jinja2 extensions in our application's configuration file (e.g. ``/src/config/development.py``).
These extensions are then used to instantiate of our Environment instance

For more detail on Jinja2 extensions, refer to `the extensions documentation <http://jinja.pocoo.org/docs/2.10/extensions/#jinja-extensions>`_

*config/development.py* :

::

    JINJA2_TEMPLATES = {
        'DEFAULT': {
            'EXTENSIONS': (
                    'tests.test_app.templatetags.TestExtension',
                )
        }
    }

Example Python code :

::

    from flask_philo import app

    env_extensions = load_extensions_from_config(app.config)
    env = Environment(
        extensions=load_extensions_from_config(**env_extensions)
    )



init_filesystem_loader
############################

To list all available items within a specified S3 Bucket, we use the *list_objects_v2* method

``list_objects_v2(bucket_name, region_name)``

* **bucket_name** : Name of Amazon S3 Bucket
* **region_name** : Name of Amazon S3 Region

Example Python calling code :

::

    from flask_philo.cloud.aws.s3 import list_objects_v2

    # Retrieve bucket content
    bucket_name = 'my_data_bucket'
    region_name = 'us-west-2'
    bucket_content = list_objects_v2(bucket_name, bucket_region)['Contents']

    # Print all bucket items
    print("Bucket contents : ")
    for bucket_item in bucket_content:
        print(bucket_item['Key'])

    ##########################
    This code yields the following printed output :
    Bucket contents :
    readme.txt
    13167621.mp3
    18776371.mp3
