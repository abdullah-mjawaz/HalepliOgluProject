from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from .models import User


class AuthenticationBackend(ModelBackend):
    """ Backend Authentication"""
    def authenticate(self, request, query=None, password=None, **kwargs):  
        if  query is None or password is None:
            return None
        try:
            # Username query is case insensitive
            user_queryset = User.objects.filter(
                Q(username__iexact=query)|
                Q(email__iexact=query)
            ).distinct()
            if  user_queryset.exists() and user_queryset.count() == 1 :   
                user = user_queryset.first()
                #print('checking user password', user.check_password(password))
                if user.check_password(password) and self.user_can_authenticate(user):
                    return user
            else:
                return None
        except User.DoesNotExist:
            return None
