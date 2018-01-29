# loads dinamically all files in directory
import os

__all__ = [
    f.split('.py')[0] for f in os.listdir(os.path.dirname(__file__))
    if f.endswith('.py') and '__init__.py' != f]
