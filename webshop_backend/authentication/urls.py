from django.urls import path
from .views.register import RegisterView
from .views.login import LoginView
from .views.logout import LogoutView
from .views.get_user import UserDetailsView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('get-user/', UserDetailsView.as_view(), name='user-details'),
]
