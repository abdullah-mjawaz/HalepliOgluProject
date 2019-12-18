import jwt
from django.conf import settings
from calendar import timegm
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext as _
from rest_framework import serializers
from accounts.serializers import UserSerializer
from .utilities import (jwt_encode_handler, 
                        jwt_decode_handler,
                        jwt_payload_handler,
                        )

def jwt_response_handler(token, user=None, request=None):
    """
    Returns the response data for both the login and refresh views.
    Override to return a custom response such as including the
    serialized representation of the User.
    """
    return {
        'token': token,
        'user': UserSerializer(user).data
    }

User = get_user_model()

class JSONWebTokenSerializer(serializers.Serializer):
    """
    Serializer class used to validate a username and password.
    'username' is identified by the custom UserModel.USERNAME_FIELD.
    Returns a JSON Web Token that can be used to authenticate later calls.
    """
    email = serializers.CharField(write_only=True,
                                  required=True,
                                  allow_blank=False)
    password = serializers.CharField(write_only=True,
                                     required=True,
                                     allow_blank=False,
                                     style={'input_type': 'password'})
    remember = serializers.BooleanField(write_only=True, required=False)
    errormessages = {'invalid_login': _('Please enter a correct username and password.' 
                                        'Note that both fields may be case-sensitive.'),
                     'inactive': "This account is inactive.",
                     'E_not_verified': 'E-mail is not verified.',
                     'loginfailed': 'Unable to login with provided credentials.'
                    }   
    def __init__(self, request=None, *args, **kwargs):
        """The 'request' parameter is set for custom auth use by subclasses.
           The form data comes in via the standard 'data' kwarg."""
        self.request = request
        self.user = None
        self.token = None
        self.payload = None
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def _validate_user(self,email, password):
        """ private function to authenticate user using django backends"""
        user = None
        if email and password:
            # Authentication starts using rest_Backends
            user =  authenticate(query=email, password=password)
            #print("try to log in the user", user, password)
        else:
            raise serializers.ValidationError(detail=self.errormessages["invalid_login"],
                                              code='invalid_login')
        return user

    def validate(self, attrs):
        """ Object level validation"""
        email = attrs['email'] 
        password = attrs['password']
        self.user = self._validate_user(email, password)
        if self.user is None:
            if not self.user:
                raise serializers.ValidationError(detail=self.errormessages["loginfailed"],
                                                  code='loginfailed')     
        else:
            # Did we get back an active user?
            if not self.user.is_active:
                raise  serializers.ValidationError(detail=self.errormessages['inactive'],
                                                   code='inactive')
            # If required, is the email verified?
            elif settings.EMAIL_VERIFICATION and settings.EMAIL_VERIFICATION ==True:
                email_address = self.user.emailaddress_set.get(email=self.user.email)
                if not email_address.verified:
                    raise  serializers.ValidationError(detail=self.errormessages['E_not_verified'],
                                                       code='E_not_verified')
            self.payload = jwt_payload_handler(self.user)
            self.token = jwt_encode_handler(self.payload, self.user)
            return jwt_response_handler(self.token, self.user, self.request)

    def get_user(self):
        """return the locally stored user"""
        return self.user

class VerificationBaseSerializer(serializers.Serializer):
    """
    Abstract serializer used for verifying and refreshing JWTs.
    """
    token = serializers.CharField()
    user = None
    def validate(self, attrs):
        msg =_('Please define a validate method.')
        raise NotImplementedError(msg)
    def _check_payload(self, token):
        """
        Check payload valid (based off of JSONWebTokenAuthentication,
        may want to refactor)
        """ 
        try:
            payload = jwt_decode_handler(token)
        except jwt.ExpiredSignature:
            msg = _('Signature has expired.')
            raise serializers.ValidationError(msg)
        except jwt.DecodeError:
            msg = _('Error decoding signature.')
            raise serializers.ValidationError(msg)
        return payload

    def _check_user(self, payload):
        """ """
        user_id = payload.get('user_id')
        if not user_id:
            msg = _('Invalid payload.')
            raise serializers.ValidationError(msg)
        # Make sure user exists
        try:
            self.user = User.objects.filter(id=user_id)[0]
        except User.DoesNotExist:
            msg = _("User doesn't exist.")
            raise serializers.ValidationError(msg)
        if not self.user.is_active:
            msg = _('User account is disabled.')
            raise serializers.ValidationError(msg)
        return self.user

    def get_user(self):
        return self.user

class VerifyJSONWebTokenSerializer(VerificationBaseSerializer):
    """
    Check the validity of an access token.
    """
    def validate(self, attrs):
        token = attrs['token']
        payload = self._check_payload(token=token)
        user = self._check_user(payload=payload)
        return {
            'token': token,
            'user': user
        }


class RefreshJSONWebTokenSerializer(VerificationBaseSerializer):
    """
    Refresh an access token.
    """
    def validate(self, attrs):
        token = attrs['token']
        payload = self._check_payload(token=token)
        user = self._check_user(payload=payload)
        # Get and check 'orig_iat'
        orig_iat = payload.get('orig_iat')

        if orig_iat:
            # Verify expiration
            refresh_limit = settings.JWT_REFRESH_EXPIRATION_DELTA

            if isinstance(refresh_limit, timedelta):
                refresh_limit = (refresh_limit.days * 24 * 3600 +
                                 refresh_limit.seconds)

            expiration_timestamp = orig_iat + int(refresh_limit)
            now_timestamp = timegm(datetime.utcnow().utctimetuple())

            if now_timestamp > expiration_timestamp:
                msg = _('Signature has expired.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('orig_iat field is required.')
            raise serializers.ValidationError(msg)

        new_payload = jwt_payload_handler(user)
        new_payload['orig_iat'] = orig_iat

        return {
            'token': jwt_encode_handler(new_payload, user),
            'user': user
        }
