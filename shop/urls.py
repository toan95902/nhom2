from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib import admin
from .views import (
    home, product_list, product_detail, cart_view, add_to_cart, remove_from_cart,
    checkout, order_success, customer_login, customer_logout, customer_register, add_review, account, api_products, order_list
)
from django.conf import settings
from django.conf.urls.static import static

app_name = "shop"

urlpatterns = [
    path('', home, name='home'),  # Trang chủ
    path('products/', product_list, name='product_list'),  # Danh sách sản phẩm
    path('products/<int:product_id>/', product_detail, name='product_detail'),  # Chi tiết sản phẩm
    path('cart/', cart_view, name='cart'),  # Giỏ hàng
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),  # Thêm sản phẩm vào giỏ hàng
    path('cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),  # Xóa sản phẩm khỏi giỏ hàng
    path('checkout/', checkout, name='checkout'),  # Trang thanh toán
    path('order-success/', order_success, name='order_success'),  # Trang xác nhận đơn hàng
    # Đăng nhập và đăng xuất
    path('login/', customer_login, name='login'),
    path('logout/', customer_logout, name='logout'),
    # Đăng ký (register)
    path('register/', customer_register, name='register'),
    # Trang Admin
    path('admin/', admin.site.urls),
    path('products/<int:product_id>/add_review/', add_review, name='add_review'),
    # Tài khoản tích hợp
    path('account/', account, name='account'),
    path('api/products', api_products),
    path("orders/", order_list, name="order_list"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
