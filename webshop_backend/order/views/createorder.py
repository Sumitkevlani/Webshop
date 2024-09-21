from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ...cart.models import Cart  # Import Cart model
from ...product.models import Product  # Import Product model
from ..models import Order
from django.db import transaction


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            cart = get_object_or_404(Cart, user=request.user)
            if not cart.items:
                return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

            total_value = 0
            product_updates = []

            for cart_item in cart.items:
                product = get_object_or_404(Product, _id=cart_item['product_id'])
                if product.stock < cart_item['quantity']:
                    return Response({'error': f"Product {product.name} is out of stock."}, status=status.HTTP_400_BAD_REQUEST)

                total_value += float(product.price) * cart_item['quantity']
                product_updates.append((product, cart_item['quantity']))

            with transaction.atomic():
                order = Order.objects.create(
                    user=request.user,
                    products=[{'product_id': cart_item['product_id'], 'quantity': cart_item['quantity']} for cart_item in cart.items],
                    total_value=total_value,
                    status='Pending'
                )

                for product, quantity in product_updates:
                    product.stock -= quantity
                    product.save()

                cart.items = []
                cart.save()

            return Response({
                'message': 'Order created successfully',
                'order_id': str(order._id),
                'total_value': total_value,
                'status': order.status
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
