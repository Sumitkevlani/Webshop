from django.urls import path
from .views.getitems import ViewCartView
from .views.additem import AddToCartView
from .views.removeitem import RemoveFromCartView
from .views.updateitem import UpdateCartItemView

urlpatterns = [
    path('get-cart/', ViewCartView.as_view(), name='view cart'),
    path('add-to-cart/', AddToCartView.as_view(), name='add to cart'),
    path('remove-from-cart/', RemoveFromCartView.as_view(), name='remove from cart'),
    path('update-cart/', UpdateCartItemView.as_view(), name='update cart'),
]
