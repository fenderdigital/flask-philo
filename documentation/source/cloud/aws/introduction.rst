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

Flask-Philo supports the use of Amazon's S3 file storage buckets, and provides a number of useful methods for storing and retrieving data

Retrieving available Bucket contents
############################

To list all available items within a specified S3 Bucket, we use the ``list_objects_v2(bucket_name, region_name)`` method:

* **bucket_name** : Name of Amazon S3 Bucket
* **region_name** : Name of Amazon S3 Region

For example:

::

    from flask_philo.cloud.aws.s3 import list_objects_v2

    bucket_name = 'bdd_reports'
    region_name = 'us-west-2'
    bucket_content = list_objects_v2(bucket_name, bucket_region)['Contents']
    for bucket_item in bucket_content:
        print(bucket_item['Key'])


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



------------



Amazon SQS
------------------------------


Sending a Message
#################

To send a message to a queue:

::

    ...
    from flask_philo.cloud.aws.sqs import send_message
    data = send_message(queue_url="https://us-west-2.queue.amazonaws.com/523525905522/new_test_queue", message_body="My new test message", region="us-west-2")

    return self.json_response(
        status=200, data=data['MessageId'])


It will print the id four our brand new message.



Sending a Message Batch
#######################

To send more than one message to a queue, we can a piece of code like the one below:

::

    ...
    from flask_philo.cloud.aws.sqs import send_message_batch
    data = send_message_batch(queue_url="https://us-west-2.queue.amazonaws.com/523525905522/new_test_queue",
        entries=[{"Id":"1","MessageBody":"[message one]"},{"Id":"2","MessageBody":"[message two]"}],
        region="us-west-2")

    return self.json_response(
        status=200, data=data)


It will return a json string coitaining the id for every message sent.


Receive Messages
#################

To receive one message from the queue:

::

    ...
    from flask_philo.cloud.aws.sqs import receive_message
    data = receive_message(queue_url="https://us-west-2.queue.amazonaws.com/523525905522/new_test_queue", region="us-west-2")

    return self.json_response(
        status=200, data=data['Messages'][0]['Body'])


In the example above, it returned the body of the message received.

To receive more than one message from the queue we can specify the attribute `` when calling the function. Like the example below:

::

    ...
    from flask_philo.cloud.aws.sqs import receive_message
    messages = receive_message(queue_url="https://us-west-2.queue.amazonaws.com/523525905522/new_test_queue", region="us-west-2", max_number_of_messages=2)

    return self.json_response(
        status=200, data=messages)



Listing Available Queues
#########################

::

    ...
    from flask_philo.cloud.aws.sqs import list_queues
    data = list_queues()

    return self.json_response(
        status=200, data=data)


Create a New Queue
##################

To create new queue via code:

::

    ...
    from flask_philo.cloud.aws.sqs import create_queue
    data = create_queue("new_test_queue", "us-west-2")

    return self.json_response(status=200, data=data['QueueUrl'])


It will return the new queue URL.


Purge Queue
############

To purge the queue we can use the following piece of code:

::

    from flask_philo.cloud.aws.sqs import purge_queue
    purge_queue(queue_url="https://us-west-2.queue.amazonaws.com/523525905522/new_test_queue")


No messages will be in the queue after that.


Delete Queue
############

We can also delete a queue by using the following piece of code:

::

    from flask_philo.cloud.aws.sqs import delete_queue
    delete_queue(queue_url="https://us-west-2.queue.amazonaws.com/523525905522/new_test_queue")


After that, we won't see the queue when we list all the queues available.


External Resources
-----------------------

* `AWS SDK Boto3 <https://pypi.python.org/pypi/boto3>`_

* `AWS <https://aws.amazon.com/>`_
