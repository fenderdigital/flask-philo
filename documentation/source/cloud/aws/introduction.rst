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


Downloading a file from an S3 Bucket
###################################

Individual S3 data items may be retrieved using the *download_file* method

``download_file(destination_filename, bucket_name, source_key, bucket_region)``

* **destination_filename** : Local, writable file location for downloaded file
* **bucket_name** : Name of Amazon S3 Bucket
* **source_key** : Amazon S3 key for the desired bucket item
* **region_name** : Name of Amazon S3 Region

Example Python calling code :

::

    from flask_philo.cloud.aws.s3 import download_file, list_objects_v2

    # Retrieve first bucket item
    bucket_name = 'my_data_bucket'
    region_name = 'us-west-2'
    bucket_item = list_objects_v2(bucket_name, region_name)['Contents'][0]

    # Download bucket item to new file location "dest/my_new_local_file.txt"
    download_file('dest/my_new_local_file.txt', bucket_name, bucket_item['Key'], region_name)


Uploading a file to an S3 Bucket
###############################

Individual files may be uploaded to an S3 bucket using the *upload_file* method

``upload_file(source_filename, bucket_name, destination_key, bucket_region)``

* **source_filename** : Local, readable file location as source of upload
* **bucket_name** : Name of Amazon S3 Bucket
* **destination_key** : New Amazon S3 key for the uploaded bucket item
* **region_name** : Name of Amazon S3 Region

Example Python calling code :

::

    from flask_philo.cloud.aws.s3 import upload_file, list_objects_v2

    bucket_name = 'my_data_bucket'
    region_name = 'us-west-2'

    # Upload new file to S3 Bucket using Key 'My_New_File_Key'
    upload_file('dest/my_new_local_file.txt', bucket_name, 'My_New_File_key', region_name)


Uploading a folder to an S3 Bucket
#################################

Bulk uploads of an entire directory's contents is possible using the *upload_dir* method

``upload_dir(source_dir, bucket_name, region_name)``

* **source_dir** : Local, readable directory containing all files for upload
* **bucket_name** : Name of Amazon S3 Bucket
* **region_name** : Name of Amazon S3 Region

Example Python code :

::

    from flask_philo.cloud.aws.s3 import upload_dir

    bucket_name = 'my_data_bucket'
    region_name = 'us-west-2'
    source_dir = './my_files/for_upload'
    upload_dir(source_dir, bucket_name, region_name)


------------



Amazon Simple Queuing Service (SQS)
------------------------------

To facilitate task queueing between software components (e.g. between multiple decoupled microservices), Flask-Philo Integrates with Amazon's Simple Queuing Service (SQS), with a number of methods for creating and managing message queuing systems.

For more detail on SQS message queuing, visit the `SQS Introduction <https://aws.amazon.com/sqs/>`_


Sending a Message
#################

Send a single message to a queue using the *send_message* method

``send_message(queue_url, message_body, region_name)``

* **queue_url** : URL for SQS queue
* **message_body** : Body of queue message
* **region** : Name of Amazon S3 Region

Example Python code :

::

    from flask_philo.cloud.aws.sqs import send_message

    queue_url = 'https://us-west-2.queue.amazonaws.com/523525905522/new_test_queue'
    message_body = 'My new test message'
    region = 'us-west-2'
    data = send_message(queue_url, message_body, region)


Sending a Message Batch
#######################

Send multiple messages to a queue using the *send_message_batch* method

``send_message_batch(queue_url, entries, region)``

* **queue_url** : URL for SQS queue
* **entries** : List of message objects, in dictionary form
* **region** : Name of Amazon S3 Region

Example Python code :

::

    from flask_philo.cloud.aws.sqs import send_message_batch

    url = 'https://us-west-2.queue.amazonaws.com/523525905522/new_test_queue'
    region = 'us-west-2'
    message_batch = [
        {"Id": "1", "MessageBody": "Test Message One"},
        {"Id": "2", "MessageBody": "Test Message Two"}
    ]

    data = send_message_batch(queue_url=url, entries=message_batch, region=region)


Retrieving Messages
#################

To retrieve a single message from a queue, use the *receive_message* method

``receive_message(queue_url, max_number_of_messages, region)``

* **queue_url** : URL for SQS queue
* **max_number_of_messages** : *Optional* Specify number of message to be retrieved
* **region** : Name of Amazon S3 Region

Example Python code :

::

    from flask_philo.cloud.aws.sqs import receive_message

    url = 'https://us-west-2.queue.amazonaws.com/523525905522/new_test_queue'
    region_name = 'us-west-2'

    retrieved_messages = receive_message(queue_url=url, region=region_name)
    print("Body of message retrieved :", retrieved_messages['Messages'][0]['Body'])

    ##########################
    This code yields the following printed output :
    Body of message retrieved : My new test message


Optionally, we may retrieve more than one message at a time using the ``max_number_of_messages`` attribute

::

    from flask_philo.cloud.aws.sqs import receive_message

    url = 'https://us-west-2.queue.amazonaws.com/523525905522/new_test_queue'
    region_name = 'us-west-2'

    retrieved_messages = receive_message(queue_url=url, region=region_name, max_number_of_messages=2)

    # Print all retrieved messages
    print("Messages : ")
    for message in retrieved_messages['Messages']:
        print(message['Body'])

    ##########################
    This code yields the following printed output :
    Messages :
    Test Message One
    Test Message Two



Listing Available Queues
#########################

To obtain a list of all available SQS queues grouped by region, use the *list_queues* method.
Note that this method may take some time to return, given that it must iteratively poll all accessible Amazon SQS regions

``list_queues()``

Example Python code :

::

    from flask_philo.cloud.aws.sqs import list_queues

    queues_by_region = list_queues()
    queue_url_list = queues_by_region['us-west-2']['QueueUrls']

    print("Queue URLs :")
    for queue_url in queue_url_list:
        print(queue_url)

    ##########################
    This code yields the following printed output :
    Queue URLs :
    https://us-west-2.queue.amazonaws.com/523525905522/test_queue
    https://us-west-2.queue.amazonaws.com/523525905522/new_test_queue
    https://us-west-2.queue.amazonaws.com/523525905522/my-priority-list










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
