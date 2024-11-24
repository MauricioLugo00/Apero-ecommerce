from django.db import models
from store.models import Product, Variation
from accounts.models import Account
from django.core.validators import MinValueValidator
from decimal import Decimal


# Modelo para el carrito de compras
class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True, db_index=True)  # Identificador único del carrito, indexado para mejorar el rendimiento de consultas
    date_added = models.DateTimeField(auto_now_add=True)  # Fecha y hora en que se agregó el carrito, se establece automáticamente

    class Meta:
        ordering = ['-date_added']  # Orden predeterminado por fecha de adición en orden descendente
        verbose_name = 'Carrito'  # Nombre legible para el modelo en singular
        verbose_name_plural = 'Carritos'  # Nombre legible para el modelo en plural

    def __str__(self):
        return f'Carrito {self.cart_id}'  # Representación en cadena del carrito

# Modelo para los ítems del carrito
class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)  # Relación con el usuario, puede ser nulo
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Relación con el producto, no puede ser nulo
    variation = models.ManyToManyField(Variation, blank=True)  # Variaciones del producto, opcional
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)  # Relación con el carrito, puede ser nulo
    quantity = models.IntegerField(validators=[MinValueValidator(1)])  # Cantidad del producto, con un valor mínimo de 1
    is_active = models.BooleanField(default=True, db_index=True)  # Estado del ítem, indexado para mejorar el rendimiento de consultas
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha y hora de creación, se establece automáticamente
    updated_at = models.DateTimeField(auto_now=True)  # Fecha y hora de última actualización, se actualiza automáticamente

    class Meta:
        ordering = ['-created_at']  # Orden predeterminado por fecha de creación en orden descendente
        verbose_name = 'Item del carrito'  # Nombre legible para el modelo en singular
        verbose_name_plural = 'Items del carrito'  # Nombre legible para el modelo en plural

    def sub_total(self):
        return self.product.price * self.quantity  # Calcula el subtotal del ítem en el carrito

    def __str__(self):
        return f'{self.quantity}x {self.product.product_name}'  # Representación en cadena del ítem del carrito
    
    @property
    def sub_total(self):
        """Calcula el subtotal para este ítem del carrito"""
        return Decimal(str(self.product.price)) * Decimal(str(self.quantity))
