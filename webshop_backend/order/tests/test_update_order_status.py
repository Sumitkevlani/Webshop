from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from bson import ObjectId
from bson.decimal128 import Decimal128
from ..models import Order
from ...authentication.models import User
from ...product.models import Product
from decimal import Decimal

class UpdateOrderStatusTests(APITestCase):

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


        # Create products
        self.product1 = Product.objects.create(_id=ObjectId(), name="Product 1", price=100.00, stock=10)
        self.product2 = Product.objects.create(_id=ObjectId(), name="Product 2", price=50.00, stock=5)

        # Create an order for the user
        self.order = Order.objects.create(
            _id=ObjectId(), user=self.user,
            products=[{'product_id': self.product1._id, 'quantity': 1}],
            total_value=100.00, status='Pending'
        )
        
        # URL for updating order status
        self.url = reverse('update order status', kwargs={'order_id': str(self.order._id)})

    # def test_update_order_status_success(self):
    #     """Test successfully updating the status of an order"""
    #     response = self.client.put(self.url, data={'status': 'Processed'}, format='json')
    #     print(response.status_code,response.data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['message'], 'Order status updated')

    #     # Check if the order's status is updated in the database
    #     self.order.refresh_from_db()
    #     self.assertEqual(self.order.status, 'Processed')

    def test_update_order_status_invalid_status(self):
        """Test updating the order status with an invalid status value"""
        response = self.client.put(self.url, data={'status': 'InvalidStatus'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid status')

    def test_update_order_status_with_total_value(self):
        """Test updating the order status and total value"""
        response = self.client.put(self.url, data={'status': 'Shipped', 'total_value': 120.50}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Order status updated')

        # Check if the order's status and total_value are updated in the database
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'Shipped')
        self.assertEqual(self.order.total_value, Decimal128('120.50'))

    def test_update_order_status_invalid_total_value(self):
        """Test updating the total value with an invalid value"""
        response = self.client.put(self.url, data={'status': 'Shipped', 'total_value': 'invalid_decimal'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_order_status_order_not_found(self):
        """Test updating status for an order that doesn't exist"""
        invalid_order_url = reverse('update order status', kwargs={'order_id': str(ObjectId())})  # Invalid ObjectId
        response = self.client.put(invalid_order_url, data={'status': 'Processed'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'No Order matches the given query.')

    def test_update_order_status_unauthenticated(self):
        """Test updating an order status without authentication"""
        self.client.logout()
        response = self.client.put(self.url, data={'status': 'Processed'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
