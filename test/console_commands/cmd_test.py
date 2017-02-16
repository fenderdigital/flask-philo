from tests.test_app.models import User


def run(app=None):
    print(User.objects.count())
    print('hello world')
