from flaskutils.views import BaseView, BaseResourceView
from flaskutils import app


class BasicHTMLView(BaseView):
    def get(self):
        return self.render_template('home.html')


class UserResourceView(BaseResourceView):

    def get(self, id=None):
        if not id:
            data = [
                {'id': 1, 'username': 'user1'},
                {'id': 2, 'username': 'user2'}
            ]
        else:
            data = {'id': 1, 'username': 'user1'}

        return self.json_response(data=data)

    def put(self, id):
        pass
