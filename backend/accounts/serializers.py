from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.conf import settings
# Get the UserModel
USER = get_user_model() 
class UserSerializer(serializers.ModelSerializer):
    """User serializer class"""
    class Meta:
        model = USER
        fields = ('id', 'username', 'email', )
        read_only_fields = ('username','password', 'groups' )

class UserCreationSerializer(serializers.Serializer):
    """ create new user serializer"""
    user = None
    errormessages = {
        'password_mismatch': "The two password fields didn't match.",
        'email_is_taken':"email is already exist",
        'username_is_taken':"username is already exist",
        'Incorrect_Group':'please enter a vaild group',
        'password_didnot_match':"The two password fields didnot match.",
        'group_not_valid':'gruop not valid',
    }
    all_groups = Group.objects.values_list('name', flat=True)
    username = serializers.CharField(
        max_length=settings.USERNAME_MAX_LENGTH,
        min_length=settings.USERNAME_MIN_LENGTH,
        required=True
    )
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(required=True, allow_blank=False,
                                      style={'input_type': 'password'})
    password2 = serializers.CharField(required=True, allow_blank=False,
                                      style={'input_type': 'password'})
    is_active = serializers.BooleanField(default=False)
    is_superuser = serializers.BooleanField(default=False)
    is_staff = serializers.BooleanField(default=False)
    group = serializers.ChoiceField(required=True, choices=all_groups)
    def clean_password(self, password):
        """
        Validates a password. You can hook into this if you want to
        restric the allowed password choices.
        """
        min_length = settings.PASSWORD_MIN_LENGTH
        if min_length and len(password) < min_length:
            raise ValidationError(("Password must be a minimum of {0} "
                                   "characters.").format(min_length))
        if validate_password(password, self.user) is not None:
            raise serializers.ValidationError(("Invalid password"))
        return password
    def validate_email(self,email):
        """validate email and check if the user is exist with a give email"""
        try:
            validate_email(email)
        except ValidationError:
            raise serializers.ValidationError(("Invalid email format"))
        qs = USER.objects.filter(email=email)
        if qs.exists():
            raise ValidationError(detail=self.errormessages['email_is_taken'],
                                  code='email_is_taken')
        return email
    def validate_username(self, username):
        """ validate the user name if the user is exist with a give username"""
        qs = USER.objects.filter(username=username)
        if qs.exists():
            raise ValidationError(detail=self.errormessages['username_is_taken'],
                                  code='username_is_taken')
        return username
    def validate_password1(self, password):
        """chech for a valid password"""
        return self.clean_password(password)
    def validate_group(self, group):
        """validated selected group"""
        if group not in  self.all_groups:
            raise ValidationError(detail=self.errormessages['group_not_valid'],
                                  code='group_not_valid')
        return group
    def validate(self, data):
        """validate at form level"""
        if data['password1'] != data['password2']:
            raise ValidationError(detail=self.errormessages['password_didnot_match'],
                                  code='password_didnot_match')
        return data
    def save(self, **kwargs):
        """Save the user isnstace"""
        email = self.validated_data.get('email')
        username = self.validated_data.get('username')
        password = self.validated_data.get('password1')
        is_active = self.validated_data.get('is_active')
        groupname = self.validated_data.get('group')
        if self.validated_data.get('is_superuser'):
            self.user = USER.objects.create_superuser(email=email, 
                                                      username=username,
                                                      is_active=is_active,
                                                      password=password) 
            self.user.save()
        elif self.validated_data.get('is_staff'):
            self.user = USER.objects.create_staffuser(email=email,
                                                      username=username, 
                                                      is_active=is_active, 
                                                      password=password)
            g = Group.objects.get(name=groupname)
            self.user.groups.add(g)
            self.user.save()
        else :
            self.user = USER.objects.create_customer(email=email, 
                                                     username=username, 
                                                     is_active=is_active, 
                                                     password=password)       
            g = Group.objects.get(name=groupname)
            self.user.groups.add(g)
            self.user.save()
        return self.user
