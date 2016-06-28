#!/bin/bash
sudo apt-get install postgresql  libpq-dev postgresql-contrib -y
sudo -u postgres psql -c "CREATE ROLE ds WITH ENCRYPTED PASSWORD 'dsps'";
sudo -u postgres psql -c "ALTER ROLE ds WITH ENCRYPTED PASSWORD 'dsps'";
sudo -u postgres psql -c "ALTER ROLE ds SET client_encoding TO 'utf8';"
sudo -u postgres psql -c "ALTER ROLE ds  WITH LOGIN;"
sudo -u postgres psql -c "ALTER ROLE ds SET default_transaction_isolation TO 'read committed';"
sudo -u postgres psql -c "ALTER ROLE ds SET timezone TO 'UTC';"
sudo -u postgres psql -c "CREATE DATABASE ds;"
sudo -u postgres psql -c "CREATE DATABASE ds_test;"
sudo -u postgres psql -c "ALTER DATABASE ds OWNER TO ds;"
sudo -u postgres psql -c "ALTER DATABASE ds_test OWNER TO ds;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ds to ds;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ds_test to ds;"
echo 'host all all  127.0.0.1/32   md5' | sudo tee -a /etc/postgresql/9.4/main/pg_hba.conf
echo "listen_addresses = 'localhost'" | sudo tee -a  /etc/postgresql/9.4/main/postgresql.conf
sudo service postgresql restart
