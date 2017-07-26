#!/bin/bash
sudo DEBIAN_FRONTEND=noninteractive apt-get -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" dist-upgrade
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install git build-essential g++ gcc vim libssl-dev libffi-dev python3-dev nginx -y
