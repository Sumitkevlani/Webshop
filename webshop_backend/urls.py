"""
URL configuration for webshop_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include,path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/',include('webshop_backend.authentication.urls')),
    path('api/product/',include('webshop_backend.product.urls')),
    path('api/cart/',include('webshop_backend.cart.urls')),
    path('api/orders/',include('webshop_backend.order.urls')),
    path('api/ai-assistant/',include('webshop_backend.ai_assistant.urls'))
]
