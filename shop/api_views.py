# Ví dụ: ecommerce/shop/api_views.py

from django.http import JsonResponse

def product_list_api(request):
    data = [
        {"id": 1, "name": "Sản phẩm A", "price": 100000},
        {"id": 2, "name": "Sản phẩm B", "price": 200000},
    ]
    return JsonResponse(data, safe=False)

def order_list_api(request):
    data = [
        {"id": 1, "customer": "Khách A", "total": 300000},
        {"id": 2, "customer": "Khách B", "total": 500000},
    ]
    return JsonResponse(data, safe=False)
