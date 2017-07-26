FROM localhost:5000/rfqa/rfqapython:v0.0.2
MAINTAINER Rondineli Gomes <rdearaujo@fender.com>


USER root

ENV PYTHONPATH = /{{project_name}}/src/

ADD ./ /{{project_name}}

RUN apt-get update && apt-get install postgresql-client -yq

RUN cp /{{project_name}}/docker/development/wait-for-it.sh /usr/bin/
RUN chmod +x /usr/bin/wait-for-it.sh

RUN rm -rf /src/*

RUN mkdir /root/.ssh

RUN cp -rf /{{project_name}}/src/.private_ssh_file/id_rsa_github /root/.ssh/id_rsa_github

RUN chmod 0600 /root/.ssh/id_rsa_github

RUN echo 'host github.com\
    HostName github.com\
    IdentityFile /root/.ssh/id_rsa_github\
    User git' > /root/.ssh/config

RUN echo 'ssh -i ~/.ssh/id_rsa_github  -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no $*' > /tmp/ssh && chmod +x /tmp/ssh

RUN GIT_TRACE=1 GIT_SSH='/tmp/ssh'  pip3 install -r /{{project_name}}/tools/requirements/dev.txt

USER root

ENV PGPASSWORD YzY4Y2MwZjRkNDcyOWVhNjYyOTc1MzVh

CMD [ "python3", "manage.py", "runserver", "--settings", "config.docker_development" ]
