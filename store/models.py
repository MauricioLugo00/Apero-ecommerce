from django.db import models
from category.models import Category
from django.urls import reverse
from accounts.models import Accounts
from django.db.models import Avg, Count


class Product(models.Model):
    product_name = models.CharField(max_length=50, null=False, unique=True)
    slug = models.SlugField(max_length=50, null=False, unique=True)
    description = models.TextField(max_length=150)
    price = models.IntegerField()
    images = models.ImageField(upload_to='photos/product', blank=True) #Cambiar a False en produccion
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])
    
    def __str__(self):
        return self.product_name
    
    def average_review(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        return reviews['average'] or 0  # Retorna 0 si no hay reseñas

    def count_reviews(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        return reviews['count'] or 0  # Retorna 0 si no hay reseñas
    
class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Accounts, on_delete=models.SET_NULL, null=True)
    subject = models.CharField(max_length=100, blank=True)
    comment = models.TextField(null=True, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject if self.subject else f'{self.user} review for {self.product}'

class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/products', max_length=255)

    def __str__(self):
        return self.product.product_name