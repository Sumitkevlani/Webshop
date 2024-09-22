from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from bson import ObjectId
from ..models import Order
from ...product.models import Product
from ...authentication.models import User

class GetAllOrdersTests(APITestCase):

    def setUp(self):
        # Create a user and authenticate them
        self.user = User.objects.create_user(username="testuser", email="testuser@gmail.com", password="TestPassword123!")
        
        # Obtain the access token for the user
        response = self.client.post('/api/auth/login/', {
            'username_or_email': 'testuser',
            'password': 'TestPassword123!'
        })
        self.token = response.data['access']

        # Set the authorization header for subsequent requests
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.url = reverse('get user-specific orders')  # Assuming the URL for GetAllOrdersView is named 'get-all-orders'

        # Create products
        self.product1 = Product.objects.create(_id=ObjectId(), name="Product 1", price=100.00, stock=10)
        self.product2 = Product.objects.create(_id=ObjectId(), name="Product 2", price=50.00, stock=5)

        # Create orders for the user
        self.order1 = Order.objects.create(
            _id=ObjectId(), user=self.user,
            products=[{'product_id': self.product1._id, 'quantity': 2}, {'product_id': self.product2._id, 'quantity': 1}],
            total_value=250.00, status='Pending'
        )

        self.order2 = Order.objects.create(
            _id=ObjectId(), user=self.user,
            products=[{'product_id': self.product1._id, 'quantity': 1}],
            total_value=100.00, status='Completed'
        )

    def test_get_all_orders_success(self):
        """Test successfully fetching all orders for the authenticated user"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # We have 2 orders created

        # Validate the first order
        order1_data = response.data[0]
        self.assertEqual(order1_data['order_id'], str(self.order1._id))
        self.assertEqual(order1_data['total_value'], 250.00)
        self.assertEqual(order1_data['status'], 'Pending')
        self.assertEqual(len(order1_data['products']), 2)  # This order has 2 products

        # Validate the second order
        order2_data = response.data[1]
        self.assertEqual(order2_data['order_id'], str(self.order2._id))
        self.assertEqual(order2_data['total_value'], 100.00)
        self.assertEqual(order2_data['status'], 'Completed')
        self.assertEqual(len(order2_data['products']), 1)  # This order has 1 product

    def test_get_all_orders_empty(self):
        """Test fetching orders when no orders exist for the user"""
        # Create a new user with no orders
        new_user = User.objects.create_user(username="newuser123", email="newuser@gmail.com", password="NewPass123!")
        # Obtain the access token for the user
        response = self.client.post('/api/auth/login/', {
            'username_or_email': 'newuser123',
            'password': 'NewPass123!'
        })
        self.token = response.data['access']

        # Set the authorization header for subsequent requests
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])  # The response should be an empty list

    def test_get_all_orders_unauthenticated(self):
        """Test fetching orders without being authenticated"""
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
