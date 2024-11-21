from django.contrib import admin
from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Configuración del administrador para el modelo Category.
    """
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'slug', 'description')
    search_fields = ('category_name', 'description')
    list_per_page = 20