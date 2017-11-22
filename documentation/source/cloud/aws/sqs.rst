AWS SQS Integration
========================

Flask-Philo supports AWS SQS integration in two ways. The former, by using
console commands to interact with AWS. The latter, by code.

Console Commands for AWS SQS Integration
-------------------------------------------


Listing Available Queues
############################

::

    python manage.py aws sqs list_queues



Create a New Queue
############################

::

    python manage.py aws sqs create_queue --region us-west-2 --queue_name priority-list


Purge Queue
#####################

::

  python manage.py aws sqs purge_queue --queue_url https://us-west-2.queue.amazonaws.com/1234562/priority-list --region us-west-2


External Resources
-----------------------

* `AWS SQS SDK Boto3 <http://boto3.readthedocs.io/en/latest/reference/services/sqs.html>`_

* `AWS SQS <https://aws.amazon.com/sqs/>`_
