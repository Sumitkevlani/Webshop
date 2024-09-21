from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from bson.decimal128 import Decimal128  # Import Decimal128 to handle MongoDB decimal
from ..models import Order  # Import the Order model
from ...authentication.models import User  # Assuming User is in the authentication app
from ...product.models import Product  # Import the Product model

class GetAllOrdersView(APIView):
    """
    API to get all orders for the authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Fetch all orders for the authenticated user
            orders = Order.objects.filter(user=request.user)
            
            # Prepare response data with order details
            orders_data = []
            
            for order in orders:
                order_items = []
                for item in order.products:
                    product = Product.objects.get(_id=item['product_id'])  # Fetch product details using product_id
                    
                    order_items.append({
                        'product_id': str(product._id),  # Convert ObjectId to string
                        'product_name': product.name,
                        'quantity': item['quantity'],
                        'price': float(product.price),  # Fetch product price
                    })

                # Prepare the final order data
                orders_data.append({
                    'order_id': str(order._id),  # Use str() for ObjectId field
                    'products': order_items,
                    'total_value': float(order.total_value.to_decimal()) if isinstance(order.total_value, Decimal128) else float(order.total_value),  # Convert Decimal128 to float
                    'status': order.status,
                    'created_at': order.created_at,
                    'updated_at': order.updated_at
                })
            
            # Return response with status 200 OK
            return Response(orders_data, status=status.HTTP_200_OK)
        except Exception as e:
            # Return a 400 Bad Request in case of any errors
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
