from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from ..models import Cart
from ...product.models import Product
from django.contrib.auth import get_user_model
from bson import ObjectId

User = get_user_model()

class UpdateCartItemTestCase(APITestCase):
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
        self.url = reverse('update cart')

        # Add a product to the cart for testing updates
        self.cart.add_item(self.product, 1)


    def test_update_cart_item_success(self):
        """Test successful update of a cart item."""
        data = {
            'product_id': str(self.product._id),
            'quantity': 5
        }
        response = self.client.put(self.url, data, format='json')
        print('Line 48:', response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Cart item updated successfully')
        
        # Verify the item's quantity was updated
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items[0]['quantity'], 5)

    def test_update_non_existent_product(self):
        """Test updating a non-existent product."""
        data = {
            'product_id': str(ObjectId()),  # Non-existent product ID
            'quantity': 1
        }
        response = self.client.put(self.url, data, format='json')
        print('Line 62:', response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_update_item_exceeds_stock(self):
        """Test updating an item to exceed available stock."""
        data = {
            'product_id': str(self.product._id),
            'quantity': 15  # Exceeds available stock (10)
        }
        response = self.client.put(self.url, data, format='json')
        print('Line 72:', response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_update_item_with_missing_fields(self):
        """Test updating an item with missing product_id or quantity."""
        data = {
            'quantity': 5
        }
        response = self.client.put(self.url, data, format='json')
        print('Line 81:', response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Both product_id and quantity are required')

    def test_update_cart_item_not_authenticated(self):
        """Test updating a cart item when user is not authenticated."""
        self.client.logout()  # Log out the user
        data = {
            'product_id': str(self.product._id),
            'quantity': 1
        }
        response = self.client.put(self.url, data, format='json')
        print('Line 92:', response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  
        self.assertIn('detail', response.data)
