#!/usr/bin/env python
"""
Example console command that outputs a count of all User objects
"""

from tests.test_app.models import User


def run(app=None):
    print(User.objects.count())
    print('hello world')
