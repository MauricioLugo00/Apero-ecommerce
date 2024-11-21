from django.urls import path
from . import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),     # URL para realizar un pedido
    path('payments/', views.payments, name='payments'),    # URL para manejar pagos
    path('order_complete/', views.order_complete, name='order_complete'),    # URL para confirmar orden completada

]