from flask_philo.db.postgresql import syncdb


def run(*args, **kwargs):
    syncdb()
