from flask_philo.commands_flask_philo import gen_salt

# ISO 8601  https://en.wikipedia.org/wiki/ISO_8601
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

DATE_FORMAT = '%Y-%m-%d'

LOG_LEVEL = 'INFO'

HOST = '127.0.0.1'

PORT = 8080

DEBUG = False

CRYP_SALT = gen_salt.run(print_salt=False)
