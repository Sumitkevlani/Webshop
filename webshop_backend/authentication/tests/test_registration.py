from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

class RegistrationTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')  # Adjust the name according to your URL configuration
        self.valid_data = {
            'username': 'validuser',
            'email': 'validuser@example.com',
            'password': 'ValidPass123!',
            'confirm_password': 'ValidPass123!'
        }

    def test_registration_success(self):
        """Test successful registration."""
        response = self.client.post(self.register_url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().username, 'validuser')
    
    def test_username_too_short(self):
        """Test for username with less than 8 characters."""
        data = self.valid_data.copy()
        data['username'] = 'short'
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_username_with_spaces(self):
        """Test username containing spaces."""
        data = self.valid_data.copy()
        data['username'] = 'invalid user'
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_username_already_exists(self):
        """Test registration with an existing username."""
        User.objects.create_user(username='existinguser', email='testuser@example.com', password='TestPassword123!')
        data = self.valid_data.copy()
        data['username'] = 'existinguser'
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_email_already_exists(self):
        """Test registration with an existing email."""
        User.objects.create_user(username='otheruser', email='validuser@example.com', password='TestPassword123!')
        data = self.valid_data.copy()
        data['email'] = 'validuser@example.com'
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_passwords_do_not_match(self):
        """Test registration with mismatched password and confirm_password."""
        data = self.valid_data.copy()
        data['confirm_password'] = 'WrongPassword123!'
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_password_validation_failure(self):
        """Test password validation (missing special character, uppercase, number)."""
        data = self.valid_data.copy()
        data['password'] = data['confirm_password'] = 'weakpass'
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    def test_internal_server_error(self):
        """Test for internal server error (unexpected failure)."""
        # You could mock a failure in the User creation logic if needed.
        pass  # Depends on how you want to handle this.
