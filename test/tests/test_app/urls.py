from .views import (
    BasicHTMLView, UserResourceView, LoginView, ProtectectView)

URLS = (
    ('/', BasicHTMLView, 'home'),
    ('/users', UserResourceView, 'user'),
    ('/users/<int:id>', UserResourceView, 'user_list'),
    ('/login', LoginView, 'login'),
    ('/protected', ProtectectView, 'protected'),
)
