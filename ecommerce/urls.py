from django.contrib import admin
from django.urls import path, include
from shop import api_views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    path('api/products', api_views.product_list_api),
    path('api/orders', api_views.order_list_api),
    path("api/", include("shop.urls")),
    path('grappelli/', include('grappelli.urls')),
]
