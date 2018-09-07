from .views import (
    BasicTemplateView, UserResourceView, RequiresBasicAuthView, RedisView,
    CorsResourceView
)

URLS = (
    ('/<template_name>', BasicTemplateView, 'home'),
    ('/users', UserResourceView, 'user'),
    ('/users/<int:id>', UserResourceView, 'user_list'),
    ('/basic_auth', RequiresBasicAuthView, 'Basic Auth'),
    ('/redis/<key>', RedisView, 'redis_item'),
    ('/cors-api/test-cors', CorsResourceView, 'cors'),

)
