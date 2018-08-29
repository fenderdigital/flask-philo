#!/usr/bin/env python
"""
Example console command that outputs a count of all User objects
"""

from tests.test_app.models import User


def run(app=None):
    user_count = User.objects.count()
    print('User count :', user_count)
