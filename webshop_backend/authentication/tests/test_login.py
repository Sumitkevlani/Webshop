from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginTestCase(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('login')
        self.user = User.objects.create_user(
            username='validuser',
            email='validuser@example.com',
            password='ValidPass123!'
        )
        self.valid_data = {
            'username_or_email': 'validuser',
            'password': 'ValidPass123!'
        }

    def test_login_with_username_success(self):
        """Test successful login with username."""
        response = self.client.post(self.login_url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_with_email_success(self):
        """Test successful login with email."""
        data = {
            'username_or_email': 'validuser@example.com',
            'password': 'ValidPass123!'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_invalid_password(self):
        """Test login with invalid password."""
        data = self.valid_data.copy()
        data['password'] = 'WrongPassword123!'
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)

    def test_nonexistent_username(self):
        """Test login with nonexistent username."""
        data = {
            'username_or_email': 'nonexistentuser',
            'password': 'ValidPass123!'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)

    def test_missing_username_or_email(self):
        """Test login without providing username or email."""
        data = {
            'username_or_email': '',
            'password': 'ValidPass123!'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)

    def test_missing_password(self):
        """Test login without providing a password."""
        data = {
            'username_or_email': 'validuser',
            'password': ''
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)

    def test_invalid_email_format(self):
        """Test login with invalid email format."""
        data = {
            'username_or_email': 'invalidemail@.com',
            'password': 'ValidPass123!'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)
