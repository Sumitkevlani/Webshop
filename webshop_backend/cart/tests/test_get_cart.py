from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from ..models import Cart
from ...product.models import Product
from django.contrib.auth import get_user_model
from bson import ObjectId

User = get_user_model()

class ViewCartTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='TestPassword123!'
        )
        self.product = Product.objects.create(
            name='Test Product',
            description='This is a test product.',
            price=19.99,
            rating=4.5,
            stock=10
        )
        # Obtain the access token for the user
        response = self.client.post('/api/auth/login/', {
            'username_or_email': 'testuser',
            'password': 'TestPassword123!'
        })
        self.token = response.data['access']

        # Set the authorization header for subsequent requests
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.cart = Cart.objects.create(user=self.user, items=[])
        self.url = reverse('view cart')

        # Add an item to the cart for testing
        self.cart.add_item(self.product, quantity=2)

    def test_view_cart_success(self):
        """Test retrieving the cart items successfully."""
        self.client.login(username='testuser', password='TestPassword123!')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = [{'product': self.product.name, 'quantity': 2}]
        self.assertEqual(response.data['cart'], expected_data)

    def test_view_cart_not_authenticated(self):
        """Test retrieving the cart without authentication."""
        self.client.logout()  # Log out the user
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_view_cart_empty(self):
        """Test retrieving an empty cart."""
        # Clear the items in the existing cart instead of creating a new one
        self.cart.items = []  # Set the items to an empty list
        self.cart.save()  # Save the changes
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['cart'], [])  # Expecting an empty cart


    def test_view_cart_no_cart_found(self):
        """Test retrieving a cart when the user has no cart."""
        self.cart.delete()  # Delete the cart for the user
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'No Cart matches the given query.')
