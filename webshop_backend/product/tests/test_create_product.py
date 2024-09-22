from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from ..models import Product

class ProductCreateTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('create product')

    def test_create_product_success(self):
        """Test successful creation of a product."""
        data = {
            'name': 'Test Product',
            'description': 'This is a test product.',
            'price': 19.99,
            'rating': 4.5,
            'stock': 10
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, 'Test Product')

    def test_create_product_invalid_price(self):
        """Test creating a product with invalid price."""
        data = {
            'name': 'Test Product',
            'description': 'This is a test product.',
            'price': -5.0,  # Invalid price
            'rating': 4.5,
            'stock': 10
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)

    def test_create_product_invalid_rating(self):
        """Test creating a product with invalid rating."""
        data = {
            'name': 'Test Product',
            'description': 'This is a test product.',
            'price': 19.99,
            'rating': 6.0,  # Invalid rating
            'stock': 10
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)

    def test_create_product_invalid_stock(self):
        """Test creating a product with invalid stock."""
        data = {
            'name': 'Test Product',
            'description': 'This is a test product.',
            'price': 19.99,
            'rating': 4.5,
            'stock': 0  # Invalid stock
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)

    def test_create_product_missing_fields(self):
        """Test creating a product with missing fields."""
        data = {
            'name': '',  # Missing name
            'description': 'This is a test product.',
            'price': 19.99,
            'rating': 4.5,
            'stock': 10
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
