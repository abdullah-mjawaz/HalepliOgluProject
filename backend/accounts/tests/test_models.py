from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):

    def test_create_staffuser_with_email(self):
        """test if the user created with email successfully"""
        email="abdo@gmail.com"
        password="a123456"
        user = get_user_model().objects.create_staffuser(
            email=email,
            password=password,
            username='abdoprincem'
        )
        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_superuser_with_email(self):
        """test if the user created with email successfully"""
        email = "abdo@gmail.com"
        password = "a123456"
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password,
            
        )
        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


    def test_create_customer_with_email(self):
        """test if the user created with email successfully"""
        email="abdo@gmail.com"
        password="a123456"
        user = get_user_model().objects.create_customer(
            email=email,
            password=password,
            username='abdoprincem'
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
    def test_new_user_email_normalized(self):
        """test if the user's email is normalized"""
        email = "abdo@GMAIL.COM"
        password = "a123456"
        user = get_user_model().objects.create_customer(
            email=email,
            password=password,
            username='abdoprincem'
        )
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """test if the invalid email pass"""
        with self.assertRaises(ValueError):
            user = get_user_model().objects.create_customer(
                email=None,
                password='a123456',
                username='abdoprincem'
            )

    def test_new_user_invalid_password(self):
        """test if the invalid email pass"""
        with self.assertRaises(ValueError):
            user = get_user_model().objects.create_customer(
                email='abdo@gmail.com',
                password=None,
                username='abdoprincem'
            )
            
        