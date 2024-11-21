from django.contrib import admin
from .models import Cart, CartItem

# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'date_added')
    search_fields = ('cart_id',)  # Añadir campo de búsqueda por cart_id
    list_filter = ('date_added',)  # Añadir filtro por fecha de añadido

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity', 'is_active')
    search_fields = ('product__product_name', 'cart__cart_id')  # Añadir campos de búsqueda por producto y cart_id
    list_filter = ('is_active', 'product')  # Añadir filtros por estado y producto

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
