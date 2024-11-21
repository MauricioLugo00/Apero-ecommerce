from django.db import models
from accounts.models import Account
from store.models import Product, Variation

# Modelo para gestionar los pagos
class Payment(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pendiente'),
        ('COMPLETED', 'Completado'),
        ('FAILED', 'Fallido'),
    )
    
    user = models.ForeignKey(Account, on_delete=models.CASCADE)  # Usuario que realiza el pago
    payment_id = models.CharField(max_length=100)  # Identificador del pago
    payment_method = models.CharField(max_length=100)  # Método de pago utilizado
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)  # Cantidad pagada
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')  # Estado del pago
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación del pago

    def __str__(self):
        return self.payment_id  # Representación en cadena del pago

# Modelo para gestionar los pedidos
class Order(models.Model):
    STATUS = (
        ('New', 'Nuevo'),
        ('Accepted', 'Aceptado'),
        ('Completed', 'Completado'),
        ('Cancelled', 'Cancelado'),
    )

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)  # Usuario que realiza el pedido
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)  # Pago asociado al pedido
    order_number = models.CharField(max_length=20)  # Número de pedido
    first_name = models.CharField(max_length=50)  # Nombre del usuario
    last_name = models.CharField(max_length=50)  # Apellido del usuario
    phone = models.CharField(max_length=15)  # Teléfono del usuario
    email = models.EmailField(max_length=50)  # Correo electrónico del usuario
    address_line_1 = models.CharField(max_length=50)  # Dirección del usuario (línea 1)
    address_line_2 = models.CharField(max_length=50, blank=True)  # Dirección del usuario (línea 2)
    country = models.CharField(max_length=50)  # País
    state = models.CharField(max_length=50)  # Estado
    city = models.CharField(max_length=50)  # Ciudad
    order_total = models.DecimalField(max_digits=10, decimal_places=2)  # Total del pedido
    tax = models.DecimalField(max_digits=10, decimal_places=2)  # Impuestos aplicados
    status = models.CharField(max_length=10, choices=STATUS, default='New')  # Estado del pedido
    ip = models.CharField(blank=True, max_length=20)  # Dirección IP del usuario
    is_ordered = models.BooleanField(default=False)  # Indicador de si el pedido ha sido realizado
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación del pedido
    updated_at = models.DateTimeField(auto_now=True)  # Fecha de última actualización del pedido

    def full_name(self):
        return f'{self.first_name} {self.last_name}'  # Devuelve el nombre completo del usuario

    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'  # Devuelve la dirección completa del usuario

    def __str__(self):
        return self.order_number  # Representación en cadena del pedido

# Modelo para los productos dentro de un pedido
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)  # Pedido al que pertenece el producto
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)  # Pago asociado al producto
    user = models.ForeignKey(Account, on_delete=models.CASCADE)  # Usuario que realizó el pedido
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Producto asociado al pedido
    variations = models.ManyToManyField(Variation, blank=True)  # Variaciones del producto
    quantity = models.IntegerField()  # Cantidad del producto en el pedido
    product_price = models.DecimalField(max_digits=10, decimal_places=2)  # Precio del producto
    ordered = models.BooleanField(default=False)  # Indicador de si el producto ha sido ordenado
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación del producto en el pedido
    updated_at = models.DateTimeField(auto_now=True)  # Fecha de última actualización del producto en el pedido

    def __str__(self):
        return self.product.name  # Representación en cadena del producto en el pedido
