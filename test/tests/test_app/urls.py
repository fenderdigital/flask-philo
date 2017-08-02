from .views import (
    BasicHTMLView, UserResourceView, RequiresBasicAuthView, RedisView
)

URLS = (
    ('/', BasicHTMLView, 'home'),
    ('/users', UserResourceView, 'user'),
    ('/users/<int:id>', UserResourceView, 'user_list'),
    ('/basic_auth', RequiresBasicAuthView, 'Basic Auth'),
    ('/redis/<key>', RedisView, 'redis_item'),
)
