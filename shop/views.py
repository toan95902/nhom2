from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order, Category, Review, OrderItem
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

def home(request):
    products = Product.objects.all()
    best_sellers = Product.objects.order_by('-sold')[:6]
    new_products = Product.objects.order_by('-created_at')[:6]
    sale_products = Product.objects.filter(discount__gt=0)[:6]
    return render(request, 'shop/home.html', {
        'best_sellers': best_sellers,
        'new_products': new_products,
        'sale_products': sale_products,
    })

def product_list(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    products = Product.objects.all()
    categories = Category.objects.all()


    if query:
        products = products.filter(name__icontains=query)
    if category_id:
        products = products.filter(category__id=category_id)

    
    return render(request, 'shop/product_list.html', {
        'products': products,
        'query': query,
        'selected_category': category_id,
        'category': categories,
    })

def product_detail(request, product_id):
    """ Chi tiết sản phẩm """
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/product_detail.html', {'product': product})

def cart_view(request):
    """ Hiển thị giỏ hàng """
    cart = request.session.get('cart', {})
    products = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = Product.objects.filter(id=product_id).first()
        if product:
            total_price += product.price * quantity
            products.append({
                'product': product,
                'quantity': quantity,
                'subtotal': product.price * quantity
            })

    return render(request, 'shop/cart.html', {'products': products, 'total_price': total_price})

def add_to_cart(request, product_id):
    """ Thêm sản phẩm vào giỏ hàng và quay lại trang hiện tại """
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    request.session.modified = True
    # Chuyển hướng về URL hiện tại (hoặc về 'shop:home' nếu không có referrer)
    return redirect(request.META.get('HTTP_REFERER', 'shop:home'))

def remove_from_cart(request, product_id):
    """ Xóa sản phẩm khỏi giỏ hàng """
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    if product_id_str in cart:
        del cart[product_id_str]
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('shop:cart')

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('shop:cart')
    
    cart_items = []
    total_price = 0
    for product_id, quantity in cart.items():
        product = Product.objects.filter(id=product_id).first()
        if product:
            total_price += product.price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': product.price * quantity
            })

    if request.method == "POST":
        fullname = request.POST.get('fullname', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        payment_method = request.POST.get('payment_method', '').strip()
        if not fullname or not phone or not address:
            return render(request, 'shop/checkout.html', {
                'cart_items': cart_items,
                'total_price': total_price,
                'error': "Vui lòng nhập đầy đủ thông tin!"
            })
        order = Order.objects.create(
            customer_name=fullname,
            address=address,
            payment_method=payment_method,
            total_price=total_price,
        )
        # Tạo OrderItem cho mỗi sản phẩm trong giỏ hàng
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['product'].price
            )
        # Sau khi tạo order và các order item, xóa giỏ hàng
        request.session['cart'] = {}
        return redirect('shop:order_success')

    return render(request, 'shop/checkout.html', {'cart_items': cart_items, 'total_price': total_price})

def order_success(request):
    """ Trang xác nhận đặt hàng thành công """
    return render(request, 'shop/order_success.html')

def customer_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('shop:home')
        else:
            messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng")
    return render(request, 'shop/customer_login.html')

def customer_logout(request):
    logout(request)
    return redirect('shop:home')

def customer_register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Kiểm tra nếu username đã tồn tại
        from django.contrib.auth.models import User
        if User.objects.filter(username=username).exists():
            messages.error(request, "Tên người dùng đã tồn tại!")
        else:
            user = User.objects.create_user(username=username, password=password)
            messages.success(request, "Đăng ký thành công! Vui lòng đăng nhập.")
            return redirect('shop:login')
    return render(request, 'shop/customer_register.html')

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        Review.objects.create(product=product, user=request.user, rating=rating, comment=comment)
        messages.success(request, "Cảm ơn bạn đã đánh giá sản phẩm!")
    return redirect('shop:product_detail', product_id=product.id)

def account(request):
    # Nếu người dùng đã đăng nhập, hiển thị thông tin tài khoản
    if request.user.is_authenticated:
        return render(request, 'shop/account.html')
    # Nếu chưa đăng nhập, hiển thị giao diện tích hợp đăng nhập và đăng ký
    return render(request, 'shop/account.html')

