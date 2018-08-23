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


Amazon S3 Bucket
-----------------

Flask-Philo supports the use of Amazon's S3 file storage buckets, and provides a number of useful methods for storing and retrieving data.

Each S3 method may be called in two ways:

* Imported and called as a standard Python function
* Invoked from the command line using ``manage.py``

...examples for both are included for every method documented below


Retrieving available Bucket contents
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
