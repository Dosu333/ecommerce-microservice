from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from user.models import Token

User = get_user_model()

class LoginTests(APITestCase):

    def setUp(self):
        self.customer = User.objects.create_user(
            email="user@example.com",
            password="testpassword",
            is_active=True,
            verified=True
        )
        self.vendor = User.objects.create_user(
            email="uservendor@example.com",
            password="testpassword",
            roles=['VENDOR'],
            is_active=True,
            verified=True
        )
        self.login_url = reverse('user:login')

    def test_valid_customer_login(self):
        """Ensure a user can log in and get a token"""
        response = self.client.post(self.login_url, {
            "email": "user@example.com",
            "password": "testpassword",
            "role": "customer"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)  # JWT token returned
        
    def test_valid_vendor_login(self):
        """Ensure a user can log in and get a token"""
        response = self.client.post(self.login_url, {
            "email": "uservendor@example.com",
            "password": "testpassword",
            "role": "vendor"
        })
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)  # JWT token returned

    def test_invalid_login(self):
        """Ensure login fails with wrong credentials"""
        response = self.client.post(self.login_url, {
            "email": "user@example.com",
            "password": "wrongpassword",
            "role": "customer"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_invalid_role_login(self):
        """Ensure login fails with wrong role"""
        response = self.client.post(self.login_url, {
            "email": "user@example.com",
            "password": "testpassword",
            "role": "Vendor"
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_unverified_user_login(self):
        """Ensure unverified user cannot login"""
        self.customer.verified = False
        self.customer.save()
        response = self.client.post(self.login_url, {
            "email": "user@example.com",
            "password": "testpassword",
            "role": "customer"
            })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TokenVerificationTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com", 
            password="password",
            is_active=True,
            verified=True
            )
        self.token = Token.objects.create(user=self.user, token="validtoken")
        self.verify_url = reverse('user:authviewsets-verify-token')

    def test_verify_valid_token(self):
        response = self.client.post(self.verify_url, {"token": "validtoken"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["valid"])

    def test_verify_invalid_token(self):
        response = self.client.post(self.verify_url, {"token": "invalidtoken"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["valid"])


class PasswordResetTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="user@example.com", password="password", is_active=True, verified=True)
        self.reset_url = reverse('user:authviewsets-initialize-reset')
        self.create_password_url = reverse('user:authviewsets-create-password')
        self.token = Token.objects.create(user=self.user, token="resettoken")

    def test_initialize_reset_valid_email(self):
        """Ensure password reset email is sent"""
        response = self.client.post(self.reset_url, {"email": "user@example.com"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Email successfully sent", response.data["message"])

    def test_initialize_reset_invalid_email(self):
        """Ensure reset fails for non-existent user"""
        response = self.client.post(self.reset_url, {"email": "wrong@example.com"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("user with this record not found", response.data["message"])

    def test_create_password_with_valid_token(self):
        """Ensure password is successfully changed"""
        response = self.client.post(self.create_password_url, {
            "token": "resettoken",
            "password": "newpassword"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newpassword"))

    def test_create_password_with_invalid_token(self):
        """Ensure password change fails for invalid token"""
        response = self.client.post(self.create_password_url, {
            "token": "invalidtoken",
            "password": "newpassword"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
