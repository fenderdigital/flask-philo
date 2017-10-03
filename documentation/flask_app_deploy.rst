NGINX and uWSGI for FlaskUtils app deployment
=============================================

0. Install the tools you will need:
-----------------------------------

Install uWSGI:

::

 sudo pip install uwsgi

Install NGINX:

::

 sudo apt-get install nginx


1. Create a flask app using flaskutils:
---------------------------------------

To quickly generate a new flaskutils project, navigate to the directory in which you want to create the project and run:

::

 flaskutils-admin startproject my_project


2. Create the WSGI Entry Point
------------------------------

Next, you will need to create a file that will serve as the entry point for your application.
This will tell your uWSGI server how to interact with the application.

For example, you can call the file ``manage_uwsgi.py``:

::

  import os
  import sys
  import argparse


  BASE_DIR = os.path.dirname(os.path.dirname(__file__))
  sys.path.append(os.path.join(BASE_DIR, '../'))


  from flaskutils import init_app, execute_command

  os.environ.setdefault('FLASKUTILS_SETTINGS_MODULE', "config.development")

  app = init_app(__name__, BASE_DIR)


3. Create a uWSGI Configuration File
------------------------------------

In order to create something robust for long-term usage. You will create a uWSGI configuration file with some options.

::

  [uwsgi]
  pythonpath = <you_code_dir>/src/
  wsgi-file = <you_code_dir>/src/manage_uwsgi.py
  enable-threads = true
  reload-on-rss=200
  cpu-affinity = 1
  reload-mercy = 20
  max-requests = 5000
  py-autoreload = 1
  processes = 8
  threads = 4
  buffer-size = 95535
  master = true
  socket=/tmp/my_project.sock
  chmod-socket = 660
  plugin=python3
  callable=app
  harakiri = 40
  vacuum = true
  die-on-term = true
  uid = www-data
  gid = www-data

Some important observations can be made here:

-  ``processes = 8`` refers to the number of worker processes that will serve actual requests;
- Since you will be using NGINX to handle client connections that will pass requests to uWSGI and the components will operate on the same computer, you will use a Unix socket. Sockets will be a more secure and faster solution;
- ``socket=/tmp/my_project.sock`` refers to the permissions on the socket, it's set this way to allow NGINX to access it;
- ``callable = app`` is the entry point into the application where the web server can call a functions with some parameters.


4. Configure NGNIX to proxy to uWSGI
------------------------------------
Create the NGNIX config file in order to establish the connection between NGNIX web server to uWSGI. This connection will be made via socket. You can call this file ``default``:

::

 server {
             server_name                    <your_nginx_server_name>;
             listen                         80;
             rewrite                        ^ https://$server_name$request_uri? permanent;
             access_log                     off;
 }

 server {
             listen                          443  ssl;
             ssl_certificate                 /etc/nginx/ssl/nginx.crt;
             ssl_certificate_key             /etc/nginx/ssl/nginx.key;
             server_name                     <your_nginx_server_name>;
             underscores_in_headers          on;

             keepalive_timeout               0;
             keepalive_requests              1000;
             client_max_body_size            20m;
             client_body_buffer_size         128k;
             server_tokens                   off;
             sendfile                        on;
             uwsgi_buffer_size               264k;
             uwsgi_buffers                   8 264k;
             uwsgi_busy_buffers_size         264k;
             uwsgi_connect_timeout           600s;
             uwsgi_read_timeout              600s;
             uwsgi_send_timeout              600s;
             uwsgi_ignore_client_abort       on;
             uwsgi_intercept_errors          on;
             uwsgi_max_temp_file_size        1024m;

             location / {
                 uwsgi_read_timeout          30s;
                 include                     uwsgi_params;
                 proxy_connect_timeout       30s;
                 proxy_send_timeout          30s;
                 proxy_read_timeout          30s;
                 send_timeout                30s;
                 uwsgi_pass                  unix:/tmp/my_project.sock;
                 proxy_http_version          1.1;
                 proxy_redirect              off;
             }
         }

         gzip_http_version                   1.1;
         gzip_vary                           on;
         gzip_comp_level                     6;
         gzip_proxied                        any;
         gzip_types                          application/javascript text/plain text/css application/json application/x-javascript text/xml application/xml application/xml+rss text/javascript;
         gzip_buffers                        16 8k;
         gzip_disable                        "MSIE [1-6].(?!.*SV1)";
         gzip_proxied                        expired no-cache no-store private auth;

You will need to create some config files to handle variables and make reference to them like this: ``<your_nginx_server_name>``.


5. Using systemd service file to manage multiple applications:
--------------------------------------------------------------

systemd will be responsible to start, stop, and keep alive the processes needed. It also:

- Provides aggressive parallelization capabilities
- Uses socket and D-Bus activation for starting services
- Offers on-demand starting of daemons
- Implements transactional dependency-based service control logic
- Tracks processes using Linux cgroups
- Supports snapshotting and restoring
- Maintains mount and automount points

You will need to create a service file, for example ``my_project.service``. This file will contain the following content:

::

  [Unit]
  Description=My Project
  After=syslog.target
  ConditionPathExists=<you_code_dir>/src/manage.py

  [Service]
  ExecReload=/bin/kill -HUP $MAINPID
  ExecStart=/usr/bin/uwsgi --ini <you_code_dir>/uwsgi.ini
  RuntimeDirectory=<you_code_dir>/
  KillMode=process
  Restart=on-failure

  [Install]
  WantedBy=multi-user.target
  Alias=my_project.service

You can configure your code deployment tool [AWS CodeDeploy (https://aws.amazon.com/codedeploy/), Heroku (http://uwsgi-docs.readthedocs.io/en/latest/tutorials/heroku_python.html), etc.] to handle these processes by adding some automated steps.

You can also configure Chef (https://www.chef.io/) to perform all the steps in an automated fashion.
