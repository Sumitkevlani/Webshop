from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class LogoutTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='TestPassword123!'
        )
        self.url = reverse('logout')
        self.client.force_authenticate(user=self.user)

    def test_logout_success(self):
        """Test successful logout."""
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
        self.assertEqual(response.data, {"detail": "Successfully logged out."})

        # Verify tokens are set to None
        self.user.refresh_from_db() #Retrieve the most up-to-date version of the user
        self.assertIsNone(self.user.refresh_token)
        self.assertIsNone(self.user.access_token)

    def test_logout_not_authenticated(self):
        """Test logout when user is not authenticated."""
        self.client.force_authenticate(user=None)  # Simulate unauthenticated user
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)  