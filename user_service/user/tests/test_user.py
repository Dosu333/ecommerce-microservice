from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

User = get_user_model()

class UserTests(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(email="admin@example.com", password="admin123")
        self.normal_user = User.objects.create_user(email="user@example.com", password="user123", is_active=True, verified=True)
        self.client.force_authenticate(user=self.admin_user) # Authenticate as an admin user

    def test_create_user(self):
        """Test creating a new user"""
        url = reverse('user:authviewsets-list')
        data = {"email": "newuser@gmail.com", "password": "testpassword"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="newuser@gmail.com").exists())

    def test_update_user(self):
        """Test updating user details"""
        url = reverse('user:authviewsets-detail', args=[self.normal_user.id])
        data = {"firstname": "UpdatedName"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.normal_user.refresh_from_db()
        self.assertEqual(self.normal_user.firstname, "UpdatedName")

    def test_delete_user(self):
        """Test deleting a user"""
        url = reverse('user:authviewsets-detail', args=[self.normal_user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.normal_user.id).exists())

