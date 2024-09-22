from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from ..models import Cart
from ...product.models import Product
from django.contrib.auth import get_user_model
from bson import ObjectId

User = get_user_model()

class AddToCartTestCase(APITestCase):
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
        self.url = reverse('add to cart')

        # Obtain the access token for the user
        response = self.client.post('/api/auth/login/', {
            'username_or_email': 'testuser',
            'password': 'TestPassword123!'
        })
        self.token = response.data['access']

        # Set the authorization header for subsequent requests
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_add_item_to_cart_success(self):
        """Test successful addition of an item to the cart."""
        product_id = str(self.product._id)
        data = {
            'product_id': product_id,
            'quantity': 2
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Item added to cart successfully')
        
        # Verify that the item was added to the cart
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(len(cart.items), 1)
        self.assertEqual(cart.items[0]['product_id'], self.product._id)
        self.assertEqual(cart.items[0]['quantity'], 2)

    def test_add_non_existent_product(self):
        """Test adding a non-existent product."""
        data = {
            'product_id': '66ed6d993014deaf386a9230',
            'quantity': 1
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "No Product matches the given query.")

    def test_add_item_exceeds_stock(self):
        """Test adding an item that exceeds available stock."""
        data = {
            'product_id': str(self.product._id),
            'quantity': 15  # Exceeds stock (only 10 available)
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_add_item_not_authenticated(self):
        """Test adding an item to the cart when user is not authenticated."""
        self.client.logout()  # Log out the user
        data = {
            'product_id': str(self.product._id),
            'quantity': 1
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # Should be forbidden
        self.assertIn('detail', response.data)
