Console Commands for AWS Integration
====================================

Flask-Philo supports AWS integration in two ways. The former, by using
console commands to interact with AWS.


Console Commands for AWS Key-Pair integration
---------------------------------------------

Listing Available Key-Pairs
###########################

To list all available key-pairs we can use the following console command line:

::

    python manage.py aws key_pair describe_key_pairs


Create a New Key-Pair
#####################

To create a new key-pair we can use the following syntax:

::

    python manage.py aws key_pair create_key_pair --key_name key-pair-name --key_dir ~/.ssh --region us-west-2



Console Commands for AWS S3 Integration
---------------------------------------

Listing objects on S3 Bucket
############################

The console command below will help us to list all available objects in a S3 bucket:

::

    python manage.py aws s3 list_objects_v2 --bucket bdd-reports --region us-west-2


Downloading a file from a S3 Bucket
###################################

We can download a file to a S3 Bucket by using the following console command line:

::

    python manage.py aws s3 download_file --bucket bdd-reports --region us-west-2 --fname test.log --key test_dir/test_file.log


Uploading a file to a S3 Bucket
###############################

We can upload a file to a S3 Bucket by using the following console command line:

::

    python manage.py aws s3 upload_file --bucket bdd-reports --region us-west-2 --fname test.log --key test_dir/test_file.log


Uploading a folder to a S3 Bucket
#################################

We can upload a folder to a S3 Bucket by using the following console command line:

::

    python manage.py aws s3 upload_dir --bucket bdd-reports --region us-west-2 --dir_name test_dir


It will return a json string.


Console Commands for AWS SQS Integration
----------------------------------------


Sending a Message
#################

We can send a message to the queue using the following syntax:

::

    python manage.py aws sqs send_message --queue_url https://us-west-2.queue.amazonaws.com/1234562/priority-list --message_body "my message" --region us-west-2


It will return a json string.


Sending a Message Batch
#######################


We can send a message batch using the following console command:

::

    python manage.py aws sqs send_message_batch -- queue_url https://us-west-2.queue.amazonaws.com/1234562/priority-list --entries "[{\"Id\":\"1\",\"MessageBody\":\"[message one]\"},{\"Id\":\"2\",\"MessageBody\":\"[message two]\"}]"  --region us-west-2



Receive Messages
#################

To receive one message from the queue:

::

    python manage.py aws sqs receive_message --queue_url https://us-west-2.queue.amazonaws.com/1234562/priority-list --region us-west-2


It will return a json string.


If we want to receive more than one message, we can use the following syntax:

::

    python manage.py aws sqs receive_message --queue_url https://us-west-2.queue.amazonaws.com/1234562/priority-list --region us-west-2 --max_number_of_messages=2


It will return a json string.


Listing Available Queues
#########################

To list all available queues we can use the following console command:

::

    python manage.py aws sqs list_queues


It will return a json string.


Create a New Queue
##################

To create a new queue, we can use the console command below:

::


    python manage.py aws sqs create_queue --region us-west-2 --queue_name priority-list


It will return a json string with the brand new URL, like this one: `https://us-west-2.queue.amazonaws.com/1234562/priority-list`



Purge Queue
############

To purge a queue, we can use the console command below:

::

  python manage.py aws sqs purge_queue --queue_url https://us-west-2.queue.amazonaws.com/1234562/priority-list --region us-west-2


It will return a json string.


Delete Queue
############

To delete a queue we can use the following console command:

::

    python manage.py delete_queue --queue_url https://us-west-2.queue.amazonaws.com/1234562/priority-list --region us-west-2


It will return a json string.


External Resources
-------------------

* `AWS SQS Boto3 <http://boto3.readthedocs.io/en/latest/reference/services/sqs.html>`_
* `AWS S3 Boto3 <http://boto3.readthedocs.io/en/latest/reference/services/s3.html>`_
* `AWS EC2 Boto3 <http://boto3.readthedocs.io/en/latest/reference/services/ec2.html>`_
* `AWS SQS <https://aws.amazon.com/sqs/>`_
* `AWS S3 <https://aws.amazon.com/s3/>`_
* `AWS EC2 <https://aws.amazon.com/ec2/>`_
