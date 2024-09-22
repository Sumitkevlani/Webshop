from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from ..ai_assistant_logic import ProductRetriever
from ...product.models import Product  # Import the Product model

class ProductQueryView(APIView):
    """
    API View to handle product queries from users and return relevant product IDs.
    """
    permission_classes = [AllowAny]  # Allow unrestricted access
    def post(self, request):
        
        user_query = request.data.get('query', None)
        
        if not user_query:
            return Response({'error': 'Query is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve all products from the database
            products = Product.objects.all().values('_id', 'name', 'price', 'rating')

            # Create an instance of the ProductRetriever
            retriever = ProductRetriever()
            
            # Get relevant product IDs
            relevant_product_ids = retriever.get_relevant_products(user_query, list(products))
            
            return Response({'relevant_product_ids': relevant_product_ids}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

