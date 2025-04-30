from django.contrib import admin
from django.urls import path, include
from shop import api_views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
]
