Coding for AWS Integration
==========================

Besides integrating AWS via console commands, Flask-Philo also supports AWS integration by code.


Coding for Key-Pair integration
-------------------------------

Listing Available Key-Pairs
###########################

::

    from flask_philo.cloud.aws.key_pair import describe_key_pairs
    key_pairs = describe_key_pairs()


Create a New Key-Pair
#####################

::

    from flask_philo.cloud.aws.key_pair import create_key_pair
    create_key_pair(key_name='new+key_par', key_dir='~/.ssh', region='us-west-2'):

Coding for AWS S3 Integration
------------------------------

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



Coding for AWS SQS Integration
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

    from flask_philo.cloud.aws.sqs import list_queues
    data = list_queues()

    return self.json_response(
        status=200, data=data)


Create a New Queue
##################

To create new queue via code:

::

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
-------------------

* `AWS S3 Documentation <https://docs.aws.amazon.com/cli/latest/reference/s3/>`_
* `AWS SQS Documentation <https://docs.aws.amazon.com/cli/latest/reference/sqs/>`_
* `AWS EC2 Documentation <https://docs.aws.amazon.com/cli/latest/reference/ec2/>`_
