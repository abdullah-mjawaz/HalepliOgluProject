from channels.auth import AuthMiddlewareStack
from django.urls import re_path
from channels.routing import ProtocolTypeRouter, URLRouter
#from chat.consumers  import ChatConsumer
#from notifications.consumers  import NotificationsConsumer
#from accounts.websocket_backend import JWTAuthMiddlewareStack
#from channels.auth import AuthMiddlewareStack
application = ProtocolTypeRouter({
    # (http->django views is added by default)
    #'websocket':JWTAuthMiddlewareStack(
    #    URLRouter(
    #        [
                #re_path('api/ws/chat/', ChatConsumer),
                #re_path('api/ws/chat/(?P<room_name>[^/]+)/', ChatConsumer),
                #re_path('api/ws/notifications/', NotificationsConsumer),
                #re_path('api/ws/notifications/(?P<room_name>[^/]+)/', NotificationsConsumer),
    #        ]
    #    )
    #),
})
