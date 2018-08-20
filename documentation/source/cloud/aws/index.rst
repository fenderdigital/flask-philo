AWS Integration
=======================

Flask-Philo supports basic `Amazon Web Service (AWS) <https://aws.amazon.com/>`_ integration
using Amazon's `boto3 <https://pypi.python.org/pypi/boto3>`_ AWS SDK.

More specifically, Flask-Philo provides methods for integration with two main services within Amazon's AWS family:

* **S3 Storage** - Integration with Amazon's S3 file storage buckets, providing a number of useful methods for storing and retrieving data
* **SQS Queuing** - Integration with Amazon's Simple Queuing Service (SQS), with a number of methods for creating and managing queuing systems


Settings AWS Credentials
-----------------------------------

Flask-philo supports two mechanisms for setting AWS. The
first one is via environment variables:

::

    export AWS_SECRET_ACCESS_KEY=secret_access
    export AWS_ACCESS_KEY_ID=key_id


The second one is via configuration in the settings file:

::

    AWS = {
        'credentials': {
            'aws_access_key_id': 'acces_key',
            'aws_secret_access_key': 'secret_key'
        }
    }


.. include:: ./code_integration.rst
