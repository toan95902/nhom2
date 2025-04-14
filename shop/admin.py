from django.contrib import admin
from django.utils import timezone
import datetime
from .models import Category, Product, Order, OrderItem, Cart, CartItem

# Các bộ lọc (nếu bạn đã có)
class BestSellersFilter(admin.SimpleListFilter):
    title = 'Sản phẩm bán chạy'
    parameter_name = 'best_seller'

    def lookups(self, request, model_admin):
        return (('yes', 'Có'), ('no', 'Không'),)

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(sold__gt=50)
        if self.value() == 'no':
            return queryset.exclude(sold__gt=50)
        return queryset

class NewProductsFilter(admin.SimpleListFilter):
    title = 'Sản phẩm mới'
    parameter_name = 'new'

    def lookups(self, request, model_admin):
        return (('yes', 'Có'), ('no', 'Không'),)

    def queryset(self, request, queryset):
        threshold = timezone.now() - datetime.timedelta(days=30)
        if self.value() == 'yes':
            return queryset.filter(created_at__gte=threshold)
        if self.value() == 'no':
            return queryset.exclude(created_at__gte=threshold)
        return queryset

class SaleProductsFilter(admin.SimpleListFilter):
    title = 'Sản phẩm giảm giá'
    parameter_name = 'sale'

    def lookups(self, request, model_admin):
        return (('yes', 'Có'), ('no', 'Không'),)

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(discount__gt=0)
        if self.value() == 'no':
            return queryset.filter(discount=0)
        return queryset

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'sold', 'discount', 'created_at')
    list_filter = (BestSellersFilter, NewProductsFilter, SaleProductsFilter, 'category',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

# Inline admin để hiển thị các sản phẩm trong đơn hàng
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'payment_method', 'total_price', 'created_at', 'get_products')
    inlines = [OrderItemInline]

    def get_products(self, obj):
        return ", ".join([f"{item.product.name} (x{item.quantity})" for item in obj.items.all()])
    get_products.short_description = "Sản phẩm"
