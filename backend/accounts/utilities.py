from datetime import datetime
import uuid
import jwt
from django.conf import settings
from calendar import timegm



def jwt_payload_handler(user):
    """jwt_payload_handler"""
    payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + settings.JWT_EXPIRATION_DELTA
    }
    if hasattr(user, 'email'):
        payload['email'] = user.email
    if isinstance(user.pk, uuid.UUID):
        payload['user_id'] = str(user.pk)

    payload[settings.USER_CREDENCIAL] = user.username

    # Include original issued at time for a brand new token,
    # to allow token refresh
    if settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(
            datetime.utcnow().utctimetuple()
        )
    return payload

def jwt_encode_handler(payload, user):
    """  encode the user instance into jwt header """
    key = jwt_get_secret_key(user.pk)
    enc = jwt.encode(payload, key, settings.JWT_ALGORITHM) 
    return enc


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

def jwt_decode_handler(token):
    """ get user from token, BEFORE verification, to get user secret key"""
    unverified_payload = jwt.decode(jwt=token,
                                    key=None,
                                    verify=False,
                                    algorithms=settings.JWT_ALGORITHM)
    p_k = unverified_payload.get('user_id')
    secret_key = jwt_get_secret_key(p_k)
    return jwt.decode(jwt=token, key=secret_key, algorithms=settings.JWT_ALGORITHM)
