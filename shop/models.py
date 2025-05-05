from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Danh mục sản phẩm
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Danh mục'
        verbose_name_plural = 'Danh mục'
        ordering = ['name']

# Sản phẩm
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
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # %
    description = models.TextField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='electronics')
    sold = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    @property
    def price_after_discount(self):
        return int(self.price * (1 - self.discount / 100))

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Sản phẩm'
        verbose_name_plural = 'Sản phẩm'

# Đánh giá sản phẩm
class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.product.name} by {self.user.username}"

# Đơn hàng
class Order(models.Model):
    PAYMENT_METHODS = [
        ('cod', 'Thanh toán khi nhận hàng'),
        ('momo', 'Ví MoMo'),
        ('bank', 'Chuyển khoản ngân hàng'),
    ]

    customer_name = models.CharField(max_length=255)
    address = models.TextField()
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS)
    total_price = models.DecimalField(max_digits=10, decimal_places=0, editable=False, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.customer_name}"

    def update_total_price(self):
        total = sum([item.final_price for item in self.items.all()])
        self.total_price = total
        self.save()

# Mục trong đơn hàng
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Giá gốc

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def final_price(self):
        return int(self.quantity * self.price * (1 - self.product.discount / 100))

# Giỏ hàng
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    products = models.ManyToManyField(Product, through='CartItem')

    def __str__(self):
        return f"Cart của {self.user}" if self.user else "Cart của khách vãng lai"

# Sản phẩm trong giỏ hàng
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def total_price(self):
        return int(self.quantity * self.product.price_after_discount)
