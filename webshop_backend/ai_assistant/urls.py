from django.urls import path
from .views.productquery import ProductQueryView


urlpatterns = [
    path('query/', ProductQueryView.as_view(), name='product query'),
]
