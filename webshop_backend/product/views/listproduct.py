from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Product
from ..serializers import ProductSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ['name', 'description']
    filterset_fields = {
        'price': ['exact', 'lt', 'gt'],
        'rating': ['exact', 'lt', 'gt'],
    }
    permission_classes = [AllowAny]  # Allow any user (authenticated or not)