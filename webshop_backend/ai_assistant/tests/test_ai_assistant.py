from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch
from bson import ObjectId
from ...product.models import Product
from ..ai_assistant_logic import ProductRetriever

class AIAssistantTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.query_url = reverse('product query') # Adjust according to your actual URL

        # Mock product data (as if coming from MongoDB)
        self.product1 = Product.objects.create(name='Laptop A', price=95000, rating=4.5, stock=10)
        self.product2 = Product.objects.create(name='Laptop B', price=75000, rating=4.3, stock=10)
        self.product3 = Product.objects.create(name='Laptop C', price=120000, rating=4.1, stock=10)
        self.product4 = Product.objects.create(name='Laptop D', price=60000, rating=4.0, stock=10)
        self.product5 = Product.objects.create(name='Laptop E', price=50000, rating=3.5, stock=10)

        self.mock_products = [self.product1, self.product2, self.product3, self.product4, self.product5]

        # Format product IDs as strings for response checking
        self.expected_product_ids = [str(product._id) for product in self.mock_products[:2]]

    # Mock the ProductRetriever and database query
    def test_product_query_retrieval(self):
        """
        Test AI assistant integration with the query and product retrieval.
        """
        # Test query
        response = self.client.post(self.query_url, {'query': 'laptops with rating greater than 4 and price less than 1 lakh'}, format='json')
        print(response.status_code, response.data)
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['relevant_product_ids'], self.expected_product_ids)

    def test_empty_query(self):
        """
        Test when the query is empty or missing in the request.
        """
        response = self.client.post(self.query_url, {'query': ''}, format='json')
        
        # Assertions for bad request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Query is required')
    

