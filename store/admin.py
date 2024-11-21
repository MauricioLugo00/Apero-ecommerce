from django.contrib import admin
from .models import Product, Variation, ReviewRating, ProductGallery
import admin_thumbnails

# Configuración para mostrar miniaturas en la galería de productos
@admin_thumbnails.thumbnail('image')
class ProductGalleryInLine(admin.TabularInline):
    model = ProductGallery
    extra = 1

# Configuración del administrador para productos
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category', 'is_available')  # Campos a mostrar en la lista de productos
    prepopulated_fields = {'slug': ('name',)}  # Autopopular el campo slug basado en el nombre del producto
    inlines = [ProductGalleryInLine]  # Incluir la galería de productos en línea
    search_fields = ('name', 'description', 'category__name')  # Campos para la búsqueda
    list_filter = ('category', 'is_available')  # Filtros para la lista de productos
    list_editable = ('price', 'stock', 'is_available')  # Campos editables directamente en la lista

# Configuración del administrador para variaciones de productos
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')  # Campos a mostrar en la lista de variaciones
    list_editable = ('is_active',)  # Campo editable directamente en la lista
    list_filter = ('product', 'variation_category', 'variation_value', 'is_active')  # Filtros para la lista de variaciones
    search_fields = ('product__name', 'variation_value')  # Campos para la búsqueda

# Configuración del administrador para reseñas y calificaciones
class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'status')  # Campos a mostrar en la lista de reseñas
    list_filter = ('status', 'rating')  # Filtros para la lista de reseñas
    search_fields = ('product__name', 'user__username', 'review')  # Campos para la búsqueda
    list_editable = ('status',)  # Campo editable directamente en la lista

# Configuración del administrador para la galería de productos
class ProductGalleryAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')  # Campos a mostrar en la lista de la galería
    search_fields = ('product__name',)  # Campo para la búsqueda

# Registro de los modelos en el administrador
admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating, ReviewRatingAdmin)
admin.site.register(ProductGallery, ProductGalleryAdmin)
