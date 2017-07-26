#!/bin/bash
sudo apt-get install postgresql libpq-dev postgresql-contrib -y
sudo -u postgres psql -c "CREATE ROLE riff_dev WITH ENCRYPTED PASSWORD 'dsps'";
sudo -u postgres psql -c "ALTER ROLE riff_dev WITH ENCRYPTED PASSWORD 'YzY4Y2MwZjRkNDcyOWVhNjYyOTc1MzVh'";
sudo -u postgres psql -c "ALTER ROLE riff_dev SET client_encoding TO 'utf8';"
sudo -u postgres psql -c "ALTER ROLE riff_dev WITH LOGIN;"
sudo -u postgres psql -c "ALTER ROLE riff_dev SET default_transaction_isolation TO 'read committed';"
sudo -u postgres psql -c "ALTER ROLE riff_dev SET timezone TO 'UTC';"
sudo -u postgres psql -c "CREATE DATABASE play_riffstation;"
sudo -u postgres psql -c "CREATE DATABASE play_riffstation_test;"
sudo -u postgres psql -c "ALTER DATABASE play_riffstation OWNER TO riff_dev;"
sudo -u postgres psql -c "ALTER DATABASE play_riffstation_test OWNER TO riff_dev;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE play_riffstation to riff_dev;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE play_riffstation_test to riff_dev;"
echo 'host all all  127.0.0.1/32   md5' | sudo tee -a /etc/postgresql/9.4/main/pg_hba.conf
echo "listen_addresses = 'localhost'" | sudo tee -a  /etc/postgresql/9.4/main/postgresql.conf
sudo service postgresql restart
export PGPASSWORD=YzY4Y2MwZjRkNDcyOWVhNjYyOTc1MzVh
