from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserDetailsTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='ValidPass123!'
        )
        self.url = reverse('user-details')

    def login_user(self):
        """Helper method to log in the user and return access token."""
        response = self.client.post('/api/auth/login/', {
            'username_or_email': self.user.username,
            'password': 'ValidPass123!'
        })
        return response.data['access']

    def test_get_user_details_success(self):
        """Test successful retrieval of user details."""
        access_token = self.login_user()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)
        self.assertEqual(response.data['email'], self.user.email)

    def test_get_user_details_not_authenticated(self):
        """Test retrieval of user details without authentication."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # self.assertIn('error', response.data)

    def test_get_user_details_logged_out(self):
        """Test retrieval of user details when user tokens are null."""
        # Set tokens to None and simulate a logged-out state
        self.user.refresh_token = None
        self.user.access_token = None
        self.user.save()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer invalidtoken')
        
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
