
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Điện - Đồ điện tử'),
        ('fishing', 'Đồ câu'),
        ('stationery', 'Đồ dùng học tập'),
        ('lego', 'Đồ chơi LEGO'),
        ('furniture', 'Đồ nội thất'),
    ]

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    description = models.TextField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='electronics')
    sold = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)



    def __str__(self):
        return self.name

class Order(models.Model):
    PAYMENT_METHODS = [
        ('cod', 'Thanh toán khi nhận hàng'),
        ('momo', 'Ví MoMo'),
        ('bank', 'Chuyển khoản ngân hàng'),
    ]

    customer_name = models.CharField(max_length=255)
    address = models.TextField()
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS)
    total_price = models.DecimalField(max_digits=10, decimal_places=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.customer_name}"
    
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    products = models.ManyToManyField(Product, through='CartItem')

    def __str__(self):
        return f"Cart của {self.user}" if self.user else "Cart của khách vãng lai"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review for {self.product.name} by {self.user.username}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Giá tại thời điểm mua

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
