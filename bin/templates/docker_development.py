from .development import *  # noqa
import os


PORT = int(os.environ.get("{{project_name}}_PORT", 9011))

TESTING = True

DEBUG = True

HOST = '0.0.0.0'

POSTGRESQL_DATABASE_URI = os.environ.get("DB_URI", "postgresql://riff_dev:YzY4Y2MwZjRkNDcyOWVhNjYyOTc1MzVh@db/play_riffstation")
