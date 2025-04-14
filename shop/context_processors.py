from .models import Product

def product_list(request):
    products = Product.objects.all()  # Lấy toàn bộ sản phẩm
    return {'products': products}  # Trả về context để dùng trong mọi template
