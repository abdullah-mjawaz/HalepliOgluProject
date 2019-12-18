from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)

class UserManager(BaseUserManager):
    """user Manager Class"""
    def create_user(self, email, username, is_active=False, password=None):
        """create and save new user"""
        if not email:
            raise ValueError("User must have an email address")
        if not username: 
            raise ValueError("User must have an username")
        if not password:
            raise ValueError("User must have an password ")             
        user_obj = self.model(email=self.normalize_email(email),
                              username=User.normalize_username(username),
                              is_active=is_active)
        user_obj.set_password(password)
        return user_obj

    def create_superuser(self, email, username=None, is_active=True, password=None):
        """ create superuser"""
        if username is None:
            username = email.split('@')[0]
        user = self.create_user(email, username, is_active, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, username=None, is_active=False, password=None):
        """create staffuser"""
        if username is None:
            username = email.split('@')[0]
        user = self.create_user(email, username, is_active, password=password)
        user.username = username
        user.is_superuser = False
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_customer(self, email, username, is_active=False, password=None):
        """ create customer user"""
        if username is None:
            username = email.split('@')[0]
        user = self.create_user(email, username, is_active, password=password)
        user.username = username
        user.is_superuser = False
        user.is_staff = False
        user.save(using=self._db)
        return user

class User (AbstractBaseUser, PermissionsMixin):
    """ UserModel """
    USERNAME_REGEX = '^[a-zA-Z.]*$'
    username = models.CharField(
        max_length=255,
        blank=True,
        null=False,
        unique=True,
        validators=[RegexValidator(regex=USERNAME_REGEX,
                                   message='Username name must have only characters or dot.'
                                   )])
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)    
    USERNAME_FIELD = 'email'
    REQUIRD_FIELD = []  #password and email has to be requird
    objects = UserManager()

    def __str__(self):
        return  self.email
