from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bson import ObjectId
from django.shortcuts import get_object_or_404
from ..models import Order  # Import the Order model
from decimal import Decimal  # Import Decimal for decimal operations

class UpdateOrderStatusView(APIView):
    def put(self, request, order_id):
        try:
            # Convert the string order_id from the URL to MongoDB ObjectId
            order = get_object_or_404(Order, _id=ObjectId(order_id))  # Use _id for MongoDB object lookup

            new_status = request.data.get('status')
            if new_status not in ['Pending', 'Processed', 'Shipped', 'Delivered', 'Cancelled']:
                return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Ensure total_value is a Decimal, if present
            total_value = request.data.get('total_value')
            if total_value is not None:
                try:
                    # Attempt to convert to Decimal
                    order.total_value = Decimal(total_value)
                except (ValueError, TypeError):
                    return Response({'error': 'Total value must be a valid decimal number'}, status=status.HTTP_400_BAD_REQUEST)
            order.status = new_status
            order.save()
            
            return Response({'message': 'Order status updated'}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
