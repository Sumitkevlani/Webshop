from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from ..models import Product

class ProductListTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('list products')  # Assuming the name of the URL for listing products
        self.create_products()

    def create_products(self):
        """Create sample products for testing."""
        Product.objects.create(name='Product 1', description='A great product', price=10.0, rating=4.5, stock=100)
        Product.objects.create(name='Product 2', description='Another great product', price=20.0, rating=3.5, stock=50)
        Product.objects.create(name='Product 3', description='Best product ever', price=30.0, rating=5.0, stock=0)

    def test_list_products_success(self):
        """Test successful retrieval of products."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)  # Assuming pagination returns 'results'

    def test_list_products_pagination(self):
        """Test pagination works correctly."""
        response = self.client.get(self.url, {'page_size': 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Should return 2 products

    def test_search_products(self):
        """Test searching for products by name."""
        response = self.client.get(self.url, {'search': 'Product 1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Only one matching product

    def test_filter_products_by_price(self):
        """Test filtering products by price."""
        response = self.client.get(self.url, {'price': 20.0})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Only one product with exact price

        response = self.client.get(self.url, {'price__lt': 20.0})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Should return Product 1

        response = self.client.get(self.url, {'price__gt': 20.0})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Should return Product 3

    def test_filter_products_by_rating(self):
        """Test filtering products by rating."""
        response = self.client.get(self.url, {'rating': 4.5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Only one product with exact rating

        response = self.client.get(self.url, {'rating__lt': 4.5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Should return Product 2

        response = self.client.get(self.url, {'rating__gt': 4.5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Should return Product 3

    def test_empty_results(self):
        """Test that empty results are handled correctly."""
        response = self.client.get(self.url, {'price': 100.0})  # No products at this price
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)  # Should return empty results
