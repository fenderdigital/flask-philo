from .views import (
    BasicHTMLView, UserResourceView, LoginView)

URLS = (
    ('/', BasicHTMLView, 'home'),
    ('/users', UserResourceView, 'user'),
    ('/users/<int:id>', UserResourceView, 'user_list'),
    ('/login', LoginView, 'login'),


)
