from django.urls import path
from .apps import AccountsConfig
from .views import (UserCreationView,
                    ObtainJSONWebToken,
                    RefreshJSONWebToken,
                    VerifyJSONWebToken)
app_name = AccountsConfig.name
urlpatterns = [
    path('obtain-token/', ObtainJSONWebToken.as_view(), name='obtain-token'),
    path('refresh-token/', RefreshJSONWebToken.as_view(), name='refresh-token'),
    path('verify-token/', VerifyJSONWebToken.as_view(), name='verify-token'),
    path('create/', UserCreationView.as_view(), name='user-creation-view'),
]
