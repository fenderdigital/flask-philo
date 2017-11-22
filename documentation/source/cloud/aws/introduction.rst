AWS Integration
=======================

Flask-Philo supports basic `AWS <https://aws.amazon.com/>`_ integration
using `boto3 <https://pypi.python.org/pypi/boto3>`-



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






External Resources
-----------------------

* `AWS SDK Boto3 <https://pypi.python.org/pypi/boto3>`_

* `AWS <https://aws.amazon.com/>`_
