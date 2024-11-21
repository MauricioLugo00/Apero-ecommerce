from django.db import models
from django.urls import reverse

# Modelo para las categorías de productos
class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)  # Nombre de la categoría
    description = models.TextField(max_length=255, blank=True)  # Descripción de la categoría
    slug = models.SlugField(max_length=100, unique=True)  # Slug para la URL de la categoría
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)  # Imagen de la categoría

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'  # Nombre en plural para el administrador de Django

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])  # Genera la URL para los productos por categoría

    def __str__(self):
        return self.category_name  # Representación en cadena de la categoría
