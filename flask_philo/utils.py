from flask_philo import app
from datetime import datetime


def string_to_datetime(strdate):
    """
    Receives a string as parameter and returns a formated
    datetime.
    Format is defined in the configuration parameter
    DATETIME_FORMAT by default '%Y-%m-%d %H:%M:%S'
    this format can be overide in the app configuration settings
    """
    return datetime.strptime(strdate[:19], app.config['DATETIME_FORMAT'])


def string_to_date(strdate):
    """
    Receives a string as parameter and returns a formated
    date.
    Format is defined in the configuration parameter
    DATE_FORMAT by default '%Y-%m-%d'
    this format can be overide in the app configuration settings
    """
    return datetime.strptime(strdate, app.config['DATE_FORMAT'])


def datetime_to_string(dt):
    """
    Receives a datetime as parameter and returns a formated
    string.
    Format is defined in the configuration parameter
    DATETIME_FORMAT by default '%Y-%m-%d %H:%M:%S'
    this format can be overide in the app configuration settings
    """
    return dt.strftime(app.config['DATETIME_FORMAT'])


def date_to_string(dt):
    """
    Receives a date as parameter and returns a formated
    string.
    Format is defined in the configuration parameter
    DATE_FORMAT by default '%Y-%m-%d'
    this format can be overide in the app configuration settings
    """
    return dt.strftime(app.config['DATE_FORMAT'])
