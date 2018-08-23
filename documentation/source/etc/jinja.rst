Jinja Integration
=======================

`Jinja2 <http://jinja.pocoo.org/>`_ is one of the most popular templating engines for Python, and is packaged with Flask. Flask-Philo provides a number of additional methods to facilitate common calls to the Jinja2 engine

* **set_request()** - method description here
* **render()** - Method description here
* **get_manager()** - Method description here
* **get_autoescaping_params()** - Method description here
* **load_extensions_from_config()** - Method description here
* **init_filesystem_loader()** - Method description here
* **init_loader()** - Method description here
* **init_jinja2()** - Method description here


init_jinja2
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
