import os
import pytest


def run(app, **kwargs):
    testdir = os.path.join(app.config['BASE_DIR'], 'tests')
    pytest.main(['-s', testdir])
