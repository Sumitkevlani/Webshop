from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from bson import ObjectId
from ..models import Cart
from ...product.models import Product
import json


class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        try:
            body = json.loads(request.body)
            product_id = body.get('product_id')
            quantity = body.get('quantity', 1)
            product_id = ObjectId(product_id)
            product = get_object_or_404(Product, _id=product_id)
            cart, created = Cart.objects.get_or_create(user=request.user, defaults={'items': []})

            cart.add_item(product, quantity)
            
            return Response({'message': 'Item added to cart successfully'}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated
# from django.shortcuts import get_object_or_404
# from bson import ObjectId
# from ..models import Cart
# from ...product.models import Product
# import json

# class AddToCartView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         try:
#             # Load JSON body
#             body = json.loads(request.body)
#             product_id = body.get('product_id')
#             quantity = body.get('quantity', 1)

#             # Convert product_id to ObjectId
#             product_id = ObjectId(product_id)
#             product = get_object_or_404(Product, _id=product_id)

#             # Get or create the cart
#             cart, created = Cart.objects.get_or_create(user=request.user, defaults={'items': []})

#             # Add item to cart
#             cart.add_item(product, quantity)

#             return Response({'message': 'Item added to cart successfully'}, status=status.HTTP_200_OK)
        
#         except Product.DoesNotExist:
#             return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
