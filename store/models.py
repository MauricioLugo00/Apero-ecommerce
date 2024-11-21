from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import Account
from categories.models import Category 

# Modelo para gestionar los productos
class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)  # Nombre del producto
    slug = models.SlugField(max_length=200, unique=True)  # Slug para la URL del producto
    description = models.TextField(max_length=500, blank=True)  # Descripción del producto
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Precio del producto
    images = models.ImageField(upload_to='products/')  # Imágenes del producto
    stock = models.IntegerField()  # Stock disponible del producto
    is_available = models.BooleanField(default=True)  # Indicador de disponibilidad del producto
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Categoría del producto

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])  # Genera la URL del detalle del producto

    def average_review(self):
        reviews = ReviewRating.objects.filter(product=self, status=True)
        return reviews.aggregate(models.Avg('rating'))['rating__avg'] or 0  # Calcula el promedio de las reseñas

    def count_reviews(self):
        return ReviewRating.objects.filter(product=self, status=True).count()  # Cuenta las reseñas del producto

    def __str__(self):
        return self.name  # Representación en cadena del producto

# Manager personalizado para manejar variaciones de productos
class VariationManager(models.Manager):
    def colors(self):
        return super().filter(variation_category='color', is_active=True)  # Filtra variaciones por color
    
    def sizes(self):
        return super().filter(variation_category='size', is_active=True)  # Filtra variaciones por tamaño

# Modelo para las variaciones de productos
class Variation(models.Model):
    VARIATION_CATEGORY_CHOICES = (
        ('color', 'Color'),
        ('size', 'Size'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Producto al que pertenece la variación
    variation_category = models.CharField(max_length=100, choices=VARIATION_CATEGORY_CHOICES)  # Categoría de la variación
    variation_value = models.CharField(max_length=100)  # Valor de la variación (por ejemplo, rojo, L)
    is_active = models.BooleanField(default=True)  # Indicador de si la variación está activa

    objects = VariationManager()  # Especifica el manager personalizado para variaciones

    def __str__(self):
        return f"{self.variation_value}"  # Representación en cadena de la variación

# Modelo para las reseñas y calificaciones de productos
class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Producto asociado a la reseña
    user = models.ForeignKey(Account, on_delete=models.CASCADE)  # Usuario que escribió la reseña
    subject = models.CharField(max_length=100, blank=True)  # Asunto de la reseña
    review = models.TextField(max_length=500, blank=True)  # Contenido de la reseña
    rating = models.FloatField()  # Calificación del producto
    status = models.BooleanField(default=True)  # Indicador de si la reseña está aprobada

    def __str__(self):
        return self.subject  # Representación en cadena de la reseña

# Modelo para la galería de imágenes de productos
class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Producto asociado a la imagen
    image = models.ImageField(upload_to='products/gallery/')  # Imagen del producto

    def __str__(self):
        return f"Gallery image for {self.product.name}"  # Representación en cadena de la imagen en la galería
