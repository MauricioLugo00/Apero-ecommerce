from django.db import models
from store.models import Product
from accounts.models import Accounts

class Cart(models.Model):
    user = models.ForeignKey(Accounts, on_delete=models.CASCADE, null=True, blank=True)
    cart_id = models.CharField(max_length=250, blank=True)  # Para identificar el carrito si el usuario no está registrado
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f'{self.product.product_name} - {self.quantity}'
