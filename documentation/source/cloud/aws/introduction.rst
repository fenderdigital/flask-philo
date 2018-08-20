AWS Integration
=======================

Flask-Philo supports basic `AWS <https://aws.amazon.com/>`_ integration
using `boto3 <https://pypi.python.org/pypi/boto3>`_



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


Amazon S3 Bucket support
-----------------

Flask-Philo supports the use of Amazon's S3 file storage buckets, and provides a number of useful methods for storing and retrieving data

* **add()** - create a new Flask-Philo class instance (ORM object)
* **update()** - modify an existing ORM object
* **delete()** - delete an ORM object
* **objects.get(key=value)** - retrieve an ORM object by a specified key
* **objects.filter_by(key=value)** - retrieve a collection of filtered objects by a specified key/keys
* **objects.count()** - count all object instances of a Flask-Philo class
* **objects.raw_sql(sql_query_string)** - run direct SQL queries on your application's database






External Resources
-----------------------

* `AWS SDK Boto3 <https://pypi.python.org/pypi/boto3>`_

* `AWS <https://aws.amazon.com/>`_
