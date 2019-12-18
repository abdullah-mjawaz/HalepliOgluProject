from datetime import datetime
from rest_framework.permissions import (AllowAny,)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, GenericAPIView
from .serializers import UserCreationSerializer, UserSerializer
from .auth_serializers import (JSONWebTokenSerializer,
                               RefreshJSONWebTokenSerializer,
                               VerifyJSONWebTokenSerializer)

from django.conf import settings

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

    

# Create your views here.
class UserCreationView(CreateAPIView):
    """ User account creation view """
    serializer_class = UserCreationSerializer
    permission_classes = (AllowAny,)
    def get_response_data(self, user):
        """prepare the response data todo (send a Verification email to the client) """
        if getattr(settings, 'EMAIL_VERIFICATION', True):    
            return {"detail":"Verification e-mail sent."}
        return UserSerializer(user).data

    def create(self, request, *args, **kwargs):
       
        serializer = self.serializer_class(data=self.request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(self.get_response_data(user),
                        status=status.HTTP_201_CREATED,
                        headers=headers)


class JSONWebTokenAPIView(GenericAPIView):
    """
    Base API View that various JWT interactions inherit from.
    """
    authentication_classes = ()
    permission_classes = ()
    serializer_class = None

    def post(self, request, *args, **kwargs):
        """ respose to only post requets """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.get_user()
            token = serializer.validated_data['token']
            response_data = jwt_response_handler(token, user, request)
            response = Response(response_data)
            if settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ObtainJSONWebToken(JSONWebTokenAPIView):
    """
    API View that receives a POST with a user's username and password.
    Returns a JSON Web Token that can be used for authenticated requests.
    """
    serializer_class = JSONWebTokenSerializer


class VerifyJSONWebToken(JSONWebTokenAPIView):
    """
    API View that checks the veracity of a token, returning the token if it
    is valid.
    """
    serializer_class = VerifyJSONWebTokenSerializer


class RefreshJSONWebToken(JSONWebTokenAPIView):
    """
    API View that returns a refreshed token (with new expiration) based on
    existing token
    If 'orig_iat' field (original issued-at-time) is found, will first check
    if it's within expiration window, then copy it to the new token
    """
    serializer_class = RefreshJSONWebTokenSerializer
