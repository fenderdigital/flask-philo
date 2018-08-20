AWS Integration
=======================

Flask-Philo supports basic `Amazon Web Service (AWS) <https://aws.amazon.com/>`_ integration
using Amazon's `boto3 <https://pypi.python.org/pypi/boto3>`_ AWS SDK.

More specifically, Flask-Philo provides methods for integration with two main services within Amazon's AWS family:

* **S3 Storage** - Integration with Amazon's S3 file storage buckets, providing a number of useful methods for storing and retrieving data
* **SQS Queuing** - Integration with Amazon's Simple Queuing Service (SQS), with a number of methods for creating and managing queuing systems


Settings AWS Credentials
-----------------------------------

Flask-philo supports two means of authentication for AWS. Firstly, via environment variables:

::

    $ export AWS_SECRET_ACCESS_KEY=your_secret_key
    $ export AWS_ACCESS_KEY_ID=your_access_key


...or via configuration in the settings file:


``<your_app>/config/development.py``
::

    AWS = {
        'credentials': {
            'aws_access_key_id': 'your_access_key',
            'aws_secret_access_key': 'your_secret_key'
        }
    }


Amazon S3 Bucket support
-----------------

Flask-Philo supports the use of Amazon's S3 file storage buckets, and provides a number of useful methods for storing and retrieving data

Listing available S3 Buckets
############################

::

    from flask_philo.cloud.aws.s3 import list_objects_v2

    bucket_content = list_objects_v2('bdd-reports','us-west-2')
    print(bucket_content['Name'])


Downloading a file from a S3 Bucket
###################################

::

    from flask_philo.cloud.aws.s3 import download_file

    upload_file('test.log', 'bdd-reports', 'test_dir/test.log', 'us-west-2')


Uploading a file to a S3 Bucket
###############################

::

    from flask_philo.cloud.aws.s3 import upload_file

    download_file('test.log', 'bdd-reports', 'test_dir/test.log', 'us-west-2')


Uploading a folder to a S3 Bucket
#################################

::

    from flask_philo.cloud.aws.s3 import upload_dir
    upload_dir('test_dir', 'bdd_reports', 'us-west-2')


* **add()** - create a new Flask-Philo class instance (ORM object)
* **update()** - modify an existing ORM object
* **delete()** - delete an ORM object
* **objects.get(key=value)** - retrieve an ORM object by a specified key
* **objects.filter_by(key=value)** - retrieve a collection of filtered objects by a specified key/keys
* **objects.count()** - count all object instances of a Flask-Philo class
* **objects.raw_sql(sql_query_string)** - run direct SQL queries on your application's database



.. include:: ./code_integration.rst


External Resources
-----------------------

* `AWS SDK Boto3 <https://pypi.python.org/pypi/boto3>`_

* `AWS <https://aws.amazon.com/>`_
