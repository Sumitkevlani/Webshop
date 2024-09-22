from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from bson import ObjectId
from ...product.models import Product
from ..models import Cart
import json

class RemoveFromCartView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, *args, **kwargs):
        try:
            cart = get_object_or_404(Cart, user=request.user)
            body = json.loads(request.body)
            product_id = body.get('product_id')
            product_id = ObjectId(product_id)
            
            cart.remove_item(product_id)
            return Response({'message': 'Item removed from cart successfully'}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)