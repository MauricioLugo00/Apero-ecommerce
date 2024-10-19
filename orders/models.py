from django.db import models
from accounts.models import Accounts, PAISES_LATINOAMERICANOS, DEPARTAMENTOS_LATINOAMERICA, CIUDADES_LATINOAMERICA
from store.models import Product

class Payment(models.Model):
    user = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)  
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100, default='Pendiente')  # 'Completado', 'Fallido', etc.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Payment {self.payment_id} by {self.user.email}'


class Order(models.Model):
    STATUS_CHOICES = [
        ('New', 'Nuevo'),
        ('Accepted', 'Aceptado'),
        ('Completed', 'Completado'),
        ('Cancelled', 'Cancelado'),
    ]

    user = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address_line_1 = models.CharField(max_length=100)
    address_line_2 = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=2, choices=PAISES_LATINOAMERICANOS, default='CO')
    state = models.CharField(max_length=20, choices=DEPARTAMENTOS_LATINOAMERICA, blank=False)
    city = models.CharField(max_length=50, choices=CIUDADES_LATINOAMERICA, blank=False)
    order_note = models.TextField(blank=True)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    order_status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    ip = models.GenericIPAddressField(blank=True, null=True)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_cancelled = models.BooleanField(default=False)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}, {self.city}, {self.state}, {self.country}'

    def get_order_total(self):
        """Calcula el total de la orden sumando los productos."""
        order_products = self.order_products.all()
        total = sum(item.product_price * item.quantity for item in order_products)
        self.order_total = total + self.tax  # Incluye el impuesto
        self.save()
        return self.order_total

    def cancel_order(self):
        """Cambia el estado de la orden a 'Cancelado' y reabastece los productos."""
        self.order_status = 'R'
        for order_product in self.order_products.all():
            order_product.restock()
        self.is_cancelled = True
        self.save()

    def __str__(self):
        return f'Order {self.order_number} by {self.user.email}'


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_products')
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def restock(self):
        """Repone la cantidad del producto en stock."""
        self.product.stock += self.quantity
        self.product.save()

    def __str__(self):
        return f'{self.product.product_name} ({self.quantity})'

