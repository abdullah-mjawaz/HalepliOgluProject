import json
import jwt
from datetime import datetime
import time 
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import Group
from accounts.utilities import jwt_decode_handler, jwt_encode_handler, jwt_payload_handler



CREATE_USER_URL = reverse('accounts:user-creation-view')
OBTAIN_TOKEN_URL = reverse('accounts:obtain-token')
VERIFY_TOKEN_URL = reverse('accounts:verify-token')
REFRESH_TOKEN_URL = reverse('accounts:refresh-token')

def create_user(**prams):
    """ create test user """
    u = get_user_model().objects.create_user(**prams)
    u.save()
    return u

class PublicUserApiTest(APITestCase):
    """ test the user api public"""
    def setUp(self):
        user = {
            'username':'testusername',
            'email':'testemail@test.com',
            'password':'Abdotest123',
            'is_active':True    
        }
        self.user = create_user(**user)
        self.client = APIClient()
        #create a test authentication group
        Group.objects.get_or_create(name='admins')
        Group.objects.get_or_create(name='customer')
        g = Group.objects.filter(name='admins').first()
        self.assertEqual(g.name, 'admins')
        g = Group.objects.filter(name='customer').first()
        self.assertEqual(g.name, 'customer')



    def test_create_valid_user_success(self):
        """test creating user with valid payload is successfully"""
        payload = {
            "username":"testusername1",
            "email":"testemail1@test.com",
            "password1":"Abdotest123",
            "password2":"Abdotest123",
            "is_active":True,
            "is_superuser":True,
            "is_staff":True,
            "group":"admins"
        }
        self.assertEqual(CREATE_USER_URL, '/api/accounts/create/')
        res = self.client.post(CREATE_USER_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['email'],payload['email'])

    def test_create_user_exist(self):
        """ test create user that already exist fails"""
        payload = {
            'username':'testusername',
            'email':'testemail@test.com',
            'password1':'Abdotest123',
            'password2':'Abdotest123',
            'is_active':True,
            'is_superuser': True,
            'is_staff': True,
            'group': 'customer'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_password_too_short(self):
        """test that the password must be more than 5 character"""
        payload = {
            'username':'testusername1',
            'email':'testemail1@test.com',
            'password1':'pw',
            'password2':'pw',
            'is_active':True,
            'is_superuser': True,
            'is_staff': True,
            'group': 'customer'
        }
        res = self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exist = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exist)

    def test_obtain_token_for_valid_user(self):
        """test obtain a valid JWT token for a register user"""
        payload = {
            'email':self.user.email,
            'password':'Abdotest123',
        }
        res = self.client.post(OBTAIN_TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)
        self.assertIn('id', res.data['user'])
        self.assertEqual(res.data['user']['username'], self.user.username)
        self.assertEqual(res.data['user']['email'], self.user.email)
        try:
            payload = jwt_decode_handler(res.data['token'])
        except jwt.ExpiredSignature:
            msg = 'Signature has expired.'
            self.fail(msg)
        except jwt.DecodeError:
            msg = 'Error decoding signature.'
            self.fail(msg)

    def test_verify_valid_token(self):
        """test the verify token endpoint with valid token """
        payload = {
            'email':'testemail@test.com',
            'password':'Abdotest123'
        }
        res = self.client.post(OBTAIN_TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

        payload = {
            'token':res.data['token'].decode('utf-8')
        }

        res = self.client.post(VERIFY_TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)
        self.assertIn('id', res.data['user'])
        self.assertEqual(res.data['user']['username'], self.user.username)
        self.assertEqual(res.data['user']['email'], self.user.email)
        try:
            payload = jwt_decode_handler(res.data['token'])
        except jwt.ExpiredSignature:
            msg = 'Signature has expired.'
            self.fail(msg)
        except jwt.DecodeError:
            msg = 'Error decoding signature.'
            self.fail(msg)


    def test_verify_old_expired_token(self):
        """test the verify token endpoint with expired token"""
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.'\
                'eyJ1c2VyX2lkIjoxLCJleHAiOjE1NjcxNDk1NzQsIkVt'\
                'YWlsIjoiYWJkdWxsYWgubWphd2F6QGdtYWlsLmNvbSIsIlV'\
                'zZXJuYW1lIjoiYWJkdWxsYWgubWphd2F6Iiwib3JpZ19pYXQiOjE1NjcxNDk1NzN9.'\
                'G1DCrHb0b_u-Cp_vgdDQ8uDdo3oQ74C5jpz7_N7miLE'
        payload = {
            'token': token
        }

        res = self.client.post(VERIFY_TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['non_field_errors'][0], 'Signature has expired.')

    def test_verify_old_invalid_token(self):
        """test the verify token with invalid token"""
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJyJ1c2VyX2lkIjoxLCJleHAiOjE1NjcxNDk1NzQsIkVtYWlsIjoiYWJkdWxsYWgubWphd2F6QGdtYWlsLmNvbSIsIlVzZXJuYW1lIjoiYWJkdWxsYWgubWphd2F6Iiwib3JpZ19pYXQiOjE1NjcxNDk1NzN9.G1DCrHb0b_u-Cp_vgdDQ8uDdo3oQ74C5jpz7_N7miLE'
        payload = {
            'token': token
        }
        res = self.client.post(VERIFY_TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['non_field_errors'][0], 'Error decoding signature.')

    def test_refresh_valid_token(self):
        """test refresh token end point with valid token """
        old_payload = jwt_payload_handler(self.user)
        token = jwt_encode_handler(old_payload, self.user)
        http_payload = {
            'token':token.decode('utf-8')
        }
        time.sleep(1) 
        res = self.client.post(REFRESH_TOKEN_URL, http_payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        refreshed_token = res.data['token']
        try:
            new_payload = jwt_decode_handler(refreshed_token)
        except jwt.ExpiredSignature:
            msg = 'Signature has expired.'
            self.fail(msg)
        except jwt.DecodeError:
            msg = 'Error decoding signature.'
            self.fail(msg)
        old_orig_iat = old_payload.get('orig_iat')
        new_orig_iat = new_payload.get('orig_iat')
        old_exp = old_payload.get('exp')
        new_exp = new_payload.get('exp')
        self.assertTrue(old_orig_iat == new_orig_iat)
        self.assertTrue(old_exp < new_exp)

    def test_refresh_expired_token(self):
        """ test the refresh endpoint with expired token fails """
        payload = jwt_payload_handler(self.user)
        #set the experation date in the past after stubtract the delta form time now 
        payload['exp'] = datetime.utcnow() - settings.JWT_EXPIRATION_DELTA
        token = jwt_encode_handler(payload, self.user)
        http_payload = {
            'token':token.decode('utf-8')
        }
        res = self.client.post(REFRESH_TOKEN_URL, http_payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['non_field_errors'][0], 'Signature has expired.')

    def test_refresh_invalid_token(self):
        """ test refresh token endpoint with messing payload"""
        payload = jwt_payload_handler(self.user)
        # delete the exp field 
        del payload['orig_iat']   
        token = jwt_encode_handler(payload, self.user)
        http_payload = {
            'token':token.decode('utf-8')
        }
        res = self.client.post(REFRESH_TOKEN_URL, http_payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['non_field_errors'][0], 'orig_iat field is required.')
