import jwt
from django.db.models import Q
from django.conf import settings
from django.utils.encoding import smart_text
from django.utils.translation import ugettext as _
from rest_framework import exceptions
from rest_framework.authentication import (BaseAuthentication, get_authorization_header)
from .utilities import jwt_decode_handler
from .models import User

class JSONWebTokenAuthenticationBackend(BaseAuthentication):
    """Coustom backend For Authentication using JSON WebToken JWT method"""
    www_authenticate_realm = 'api'
    def get_jwt_value(self, request):
        """ Extract the JWT value from the request Header"""
        auth = get_authorization_header(request).split()
        auth_header_prefix = settings.JWT_AUTH_HEADER_PREFIX.lower()
        if not auth:
            if settings.JWT_AUTH_COOKIE:
                return request.COOKIES.get(settings.JWT_AUTH_COOKIE)
            return None
        # compare JWT_AUTH_HEADER_PREFIX and extractd token refiex "should be like WWW-athenticate"
        if smart_text(auth[0].lower()) != auth_header_prefix:
            return None
        if len(auth) == 1:
            msg = _('Invalid Authorization header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid Authorization header. Credentials string '
                    'should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)
        #the auth list should have only 2 element which are:
        #    JWT_AUTH_HEADER_PREFIX and the token
        #return the actual token inside the header
        return auth[1]

    def authenticate(self, request):
        """Authenticate the request """
        jwt_value = self.get_jwt_value(request)
        #print('rest_authenticated has been called')
        if jwt_value is None:
            return None
        try:
            payload = jwt_decode_handler(jwt_value)
        except jwt.ExpiredSignature:
            msg = _('Signature has expired.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError:
            msg = _('Error decoding signature.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed()

        user = self.authenticate_credentials(payload) 
        return (user, payload)

    def authenticate_credentials(self, payload):
        """
        Returns an active user that matches the payload's user id and email.
        """
        username = payload.get('username')
        email = payload.get('email')
        if not username and not email:
            msg = _('Invalid payload.')
            raise exceptions.AuthenticationFailed(msg)
        try:
            # Username query is case insensitive
            user_queryset = User.objects.filter(
                Q(username__iexact=username)|
                Q(email__iexact=email)
            ).distinct()
            if  user_queryset.exists() and user_queryset.count() == 1:
                user = user_queryset.first()
                return user
        except User.DoesNotExist:
            return None      
    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        return '{0} realm="{1}"'.format(settings.JWT_AUTH_HEADER_PREFIX,
                                        self.www_authenticate_realm)
    