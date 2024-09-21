from django.urls import path
from .views.listproduct import ProductListView
from .views.createproduct import ProductCreateView

urlpatterns = [
    path('get-products/', ProductListView.as_view(), name='list products'),
    path('create-product/', ProductCreateView.as_view(), name='create product')
]
