import os
import pytest


def run(**kwargs):
    app = kwargs['app']
    testdir = os.path.join(app.config['BASE_DIR'], 'tests')
    pytest.main(['-s', testdir])
