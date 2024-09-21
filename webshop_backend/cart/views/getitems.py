from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from ..models import Cart



class ViewCartView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            cart = get_object_or_404(Cart, user=request.user)
            items = cart.get_items()
            cart_data = [{'product': item['product'].name, 'quantity': item['quantity']} for item in items]

            return Response({'cart': cart_data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
