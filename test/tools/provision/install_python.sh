#!/bin/bash
sudo apt-get install python3-pip  python3-flake8 python3-dev  -y

if [ ! ${CODE_DIR} ]; then
     echo "CODE_DIR variable is not defined"
     exit 1
else
     sudo pip3 install -r $CODE_DIR/test/requirements/dev.txt
fi
