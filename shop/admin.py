from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from django.utils.timezone import localtime
import datetime

from .models import Category, Product, Order, OrderItem, Cart, CartItem

# ------------------ Giao diện Admin ------------------
admin.site.site_header = "Shop Đồ Gia Dụng Admin"
admin.site.site_title = "Trang quản trị Shop Vip"
admin.site.index_title = "Quản lý bán hàng"

# ------------------ Bộ lọc tùy chỉnh ------------------
class BestSellersFilter(admin.SimpleListFilter):
    title = 'Sản phẩm bán chạy'
    parameter_name = 'best_seller'

    def lookups(self, request, model_admin):
        return (('yes', 'Có'), ('no', 'Không'))

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(sold__gt=50)
        elif self.value() == 'no':
            return queryset.filter(sold__lte=50)
        return queryset

class NewProductsFilter(admin.SimpleListFilter):
    title = 'Sản phẩm mới'
    parameter_name = 'new'

    def lookups(self, request, model_admin):
        return (('yes', 'Có'), ('no', 'Không'))

    def queryset(self, request, queryset):
        threshold = timezone.now() - datetime.timedelta(days=30)
        if self.value() == 'yes':
            return queryset.filter(created_at__gte=threshold)
        elif self.value() == 'no':
            return queryset.filter(created_at__lt=threshold)
        return queryset

class SaleProductsFilter(admin.SimpleListFilter):
    title = 'Sản phẩm giảm giá'
    parameter_name = 'sale'

    def lookups(self, request, model_admin):
        return (('yes', 'Có'), ('no', 'Không'))

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(discount__gt=0)
        elif self.value() == 'no':
            return queryset.filter(discount=0)
        return queryset

# ------------------ Quản lý sản phẩm ------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'thumbnail',
        'name',
        'formatted_price',
        'sold',
        'discount',
        'is_on_sale',
        'is_new',
        'created_time'
    )
    list_filter = (BestSellersFilter, NewProductsFilter, SaleProductsFilter, 'category')
    search_fields = ('name',)
    readonly_fields = ('created_time',)

    def formatted_price(self, obj):
        return f"{obj.price:,.0f}₫"
    formatted_price.short_description = 'Giá'

    def is_on_sale(self, obj):
        return obj.discount > 0
    is_on_sale.boolean = True
    is_on_sale.short_description = 'Giảm giá?'

    def is_new(self, obj):
        return obj.created_at >= timezone.now() - datetime.timedelta(days=30)
    is_new.boolean = True
    is_new.short_description = 'Mới?'

    def created_time(self, obj):
        return localtime(obj.created_at).strftime('%d/%m/%Y %H:%M')
    created_time.short_description = 'Ngày tạo'

    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="60" style="object-fit: cover; border-radius: 8px;" />', obj.image.url)
        return "Không có ảnh"
    thumbnail.short_description = 'Ảnh'

# ------------------ Quản lý danh mục ------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# ------------------ Quản lý đơn hàng ------------------
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'customer_name',
        'payment_method',
        'total_formatted',
        'created_time',
        'get_products'
    )
    inlines = [OrderItemInline]
    search_fields = ('customer_name',)

    def total_formatted(self, obj):
        return f"{obj.total_price:,.0f}₫"
    total_formatted.short_description = 'Tổng tiền'

    def created_time(self, obj):
        return localtime(obj.created_at).strftime('%d/%m/%Y %H:%M')
    created_time.short_description = 'Ngày tạo'

    def get_products(self, obj):
        return format_html("<br>".join(
            [f"<b>{item.product.name}</b> (x{item.quantity})" for item in obj.items.all()]
        ))
    get_products.short_description = "Sản phẩm"

# ------------------ Quản lý giỏ hàng ------------------
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('product', 'quantity')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_items')
    search_fields = ('user__username',)
    inlines = [CartItemInline]

    def total_items(self, obj):
        return obj.items.count()
    total_items.short_description = "Tổng mục"
