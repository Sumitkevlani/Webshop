from django.urls import path
from .views.createorder import CreateOrderView
from .views.getallorders import GetAllOrdersView
from .views.updateorderstatus import UpdateOrderStatusView

urlpatterns = [
    path('create-order/', CreateOrderView.as_view(), name='create order'),
    path('get-my-orders/', GetAllOrdersView.as_view(), name='get user-specific orders'),
    path('update-order-status/<str:order_id>/', UpdateOrderStatusView.as_view(), name='update order status'),
]
