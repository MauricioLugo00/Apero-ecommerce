from django.contrib import admin
from .models import Payment, Order, OrderProduct

class OrderProductInline(admin.TabularInline):
    """Inline configuration para productos en pedidos."""
    model = OrderProduct
    readonly_fields = ('payment', 'user', 'product', 'quantity', 'product_price', 'ordered')
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Configuración de administración para pedidos."""
    list_display = [
        'order_number', 'full_name', 'phone', 'email', 
        'city', 'order_total', 'tax', 'status', 
        'is_ordered', 'created_at'
    ]
    list_filter = ['status', 'is_ordered']
    search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'email']
    list_per_page = 20
    inlines = [OrderProductInline]

admin.site.register(Payment)
admin.site.register(OrderProduct)