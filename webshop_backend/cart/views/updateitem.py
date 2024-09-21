# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework import status
# from bson import ObjectId
# from django.shortcuts import get_object_or_404
# from ..models import Cart

# from ...product.models import Product
# import json

# class UpdateCartItemView(APIView):
#     permission_classes = [IsAuthenticated]
#     def patch(self, request, *args, **kwargs):
#         try:
#             body = json.loads(request.body)
#             product_id = body.get('product_id')
#             quantity = body.get('quantity')
#             product_id = ObjectId(product_id)

#             if not quantity or quantity < 1:
#                 return Response({'error': 'Invalid quantity'}, status=status.HTTP_400_BAD_REQUEST)

#             cart = get_object_or_404(Cart, user=request.user)
#             product = get_object_or_404(Product, _id=product_id)

#             cart.update_item(product, quantity)  # Add item method will also update the quantity

#             return Response({'message': 'Cart item updated successfully'}, status=status.HTTP_200_OK)
#         except Product.DoesNotExist:
#             return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from bson import ObjectId
from ..models import Cart
from ...product.models import Product
import json

class UpdateCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        try:
            body = json.loads(request.body)
            product_id = body.get('product_id')
            new_quantity = body.get('quantity')

            if not product_id or new_quantity is None:
                return Response({'error': 'Both product_id and quantity are required'}, status=status.HTTP_400_BAD_REQUEST)

            product_id = ObjectId(product_id)
            cart = Cart.objects.get(user=request.user)
            
            cart.update_item(product_id, new_quantity)
            
            return Response({'message': 'Cart item updated successfully'}, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'An unexpected error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
