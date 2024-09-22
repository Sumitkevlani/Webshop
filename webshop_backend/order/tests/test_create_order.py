from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from bson import ObjectId
from ..models import Order
from ...cart.models import Cart
from ...product.models import Product
from ...authentication.models import User

class CreateOrderTests(APITestCase):

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

        self.url = reverse('create order')

        # Create some products
        self.product1 = Product.objects.create(_id=ObjectId(), name="Product 1", price=100.00, stock=10, rating=4.5, description="Test product 1")
        self.product2 = Product.objects.create(_id=ObjectId(), name="Product 2", price=50.00, stock=5, rating=3.4, description="Test product 2")

        # Create a cart for the user with items
        self.cart = Cart.objects.create(user=self.user)
        self.cart.items = [{'product_id': self.product1._id, 'quantity': 2}, {'product_id': self.product2._id, 'quantity': 1}]
        self.cart.save()

    def test_create_order_success(self):
        """Test creating an order successfully when cart has items and enough stock"""
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()

        # Check the response data
        self.assertEqual(response.data['order_id'], str(order._id))
        # self.assertEqual(str(order.total_value), "250")  # 2xProduct1 (100 each) + 1xProduct2 (50)
        self.assertEqual(order.status, 'Pending')

        # Check if cart is now empty
        self.cart.refresh_from_db()
        self.assertEqual(self.cart.items, [])

        # Check if product stock is updated
        self.product1.refresh_from_db()
        self.product2.refresh_from_db()
        self.assertEqual(self.product1.stock, 8)  # Original stock (10) - quantity ordered (2)
        self.assertEqual(self.product2.stock, 4)  # Original stock (5) - quantity ordered (1)

    def test_create_order_empty_cart(self):
        """Test creating an order when the cart is empty"""
        self.cart.items = []
        self.cart.save()

        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Cart is empty')

    def test_create_order_product_out_of_stock(self):
        """Test creating an order when one product is out of stock"""
        self.product1.stock = 1  # Set product1's stock to less than the quantity in the cart
        self.product1.save()

        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], f"Product {self.product1.name} is out of stock.")

    def test_create_order_invalid_data(self):
        """Test creating an order with invalid data (manually manipulate the cart or product data)"""
        self.cart.items = [{'product_id': ObjectId(), 'quantity': 1}]  # Invalid product that doesn't exist
        self.cart.save()

        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('No Product matches the given query.', response.data['error'])

