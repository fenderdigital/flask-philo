from .views import (
    BasicHTMLView, UserResourceView, LoginView,
    ProtectectView, LogoutView, RequiresBasicAuthView
)

URLS = (
    ('/', BasicHTMLView, 'home'),
    ('/users', UserResourceView, 'user'),
    ('/users/<int:id>', UserResourceView, 'user_list'),
    ('/login', LoginView, 'login'),
    ('/protected', ProtectectView, 'protected'),
    ('/logout', LogoutView, 'logout'),
    ('/basic_auth', RequiresBasicAuthView, 'Basic Auth')
)
