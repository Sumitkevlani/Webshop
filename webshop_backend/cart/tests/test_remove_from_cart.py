from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from ..models import Cart
from ...product.models import Product
from django.contrib.auth import get_user_model
from bson import ObjectId

User = get_user_model()

class RemoveFromCartTestCase(APITestCase):
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
        self.url = reverse('remove from cart') 

        # Add a product to the cart for testing removal
        self.cart.add_item(self.product, 1)


    def test_remove_item_from_cart_success(self):
        """Test successful removal of an item from the cart."""
        data = {
            'product_id': str(self.product._id)
        }
        response = self.client.delete(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Item removed from cart successfully')

        # Verify that the item was removed from the cart
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(len(cart.items), 0)

    def test_remove_non_existent_item_from_cart(self):
        """Test removing a non-existent item from the cart."""
        data = {
            'product_id': str(ObjectId())  # Non-existent product ID
        }
        response = self.client.delete(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_remove_item_with_invalid_product_id(self):
        """Test removing an item with an invalid product_id."""
        data = {
            'product_id': 'invalid_product_id'  # Invalid product ID
        }
        response = self.client.delete(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_remove_item_not_authenticated(self):
        """Test removing an item from the cart when the user is not authenticated."""
        self.client.logout()  # Log out the user
        data = {
            'product_id': str(self.product._id)
        }
        response = self.client.delete(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
