
import jwt
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.utils.translation import ugettext as _
from django.db.models import Q
from channels.middleware import BaseMiddleware
from channels.auth import AuthMiddlewareStack, UserLazyObject
from channels.db import database_sync_to_async
from channels.sessions import CookieMiddleware, SessionMiddleware
from accounts.models import User

def jwt_decode_handler(token):
    """ get user from token, BEFORE verification, to get user secret key"""
    unverified_payload = jwt.decode(jwt=token,
                                    key=None,
                                    verify=False,
                                    algorithms=settings.JWT_ALGORITHM)
    p_k = unverified_payload.get('user_id')
    secret_key = jwt_get_secret_key(p_k)
    return jwt.decode(jwt=token, key=secret_key, algorithms=settings.JWT_ALGORITHM)


def jwt_get_secret_key(p_k=None):
    """
    For enhanced security we may want to use a secret key based on user.
    This way you have an option to logout only this user if:
        - token is compromised
        - password is changed
        - etc.
    """
    if p_k is None:
        return settings.JWT_PRIVATE_KEY

    key = settings.JWT_PRIVATE_KEY + str(p_k)
    return key


@database_sync_to_async
def get_user(token):
    """
    Return the user model instance associated with the given scope.
    If no user is retrieved, return an instance of `AnonymousUser`.
    """
    try:
        payload = jwt_decode_handler(token)
    except jwt.ExpiredSignature:
        msg = _('Signature has expired.')
        raise ValueError(msg)
    except jwt.DecodeError:
        msg = _('Error decoding signature.')
        raise ValueError(msg)
    except jwt.InvalidTokenError:
        msg = _('Invalid Token Error.')
        raise ValueError(msg)


    username = payload.get('username')
    email = payload.get('email')
    if not username and not email:
        msg = _('Invalid payload.')
        raise ValueError(msg)
    # Username query is case insensitive
    user_queryset = User.objects.filter(
        Q(username__iexact=username)|
        Q(email__iexact=email)
    ).distinct()
    if  user_queryset.exists() and user_queryset.count() == 1:
        user = user_queryset.first()
    else:   
        user = AnonymousUser()
    return user

class JWTAuthMiddleware(BaseMiddleware):
    """
    Middleware which populates scope["user"] from a Django session.
    Requires SessionMiddleware to function.
    """

    def populate_scope(self, scope):
        # Add it to the scope if it's not there already
        if "user" not in scope:
            scope["user"] = UserLazyObject()

    async def resolve_scope(self, scope):
        token = scope['path'].split('/')[4]
        print('Websocket Authenticaton in processing ')
        if token is None:
            msg = 'Token. is messing'
            scope['user'] = AnonymousUser()
            scope['Error Message'] = msg
            return self.inner(scope)
        scope["user"]._wrapped = await get_user(token)


# Handy shortcut for applying all three layers at once
JWTAuthMiddlewareStack = lambda inner: (JWTAuthMiddleware(inner))
