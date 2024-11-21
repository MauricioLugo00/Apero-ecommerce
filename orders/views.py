from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

import datetime
import json

from carts.models import CartItem
from store.models import Product
from .models import Order, Payment, OrderProduct
from .forms import OrderForm

def place_order(request):
    # Inicializar variables de cálculo
    total = 0 
    quantity = 0
    current_user = request.user
    
    # Obtener items del carrito
    cart_items = CartItem.objects.filter(user=current_user)
    
    # Validar que existan items en el carrito
    if cart_items.count() <= 0:
        return redirect('store')
    
    # Calcular totales
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    
    # Calcular impuestos y total final
    tax = round((16/100) * total, 2)
    grand_total = total + tax
    
    # Manejar el formulario de pedido
    if request.method == 'POST':
        form = OrderForm(request.POST)
        
        if form.is_valid():
            # Crear objeto de orden
            order = form.save(commit=False)
            order.user = current_user
            order.order_total = grand_total
            order.tax = tax
            order.ip = request.META.get('REMOTE_ADDR')
            order.save()
            
            # Generar número de orden
            yr = int(datetime.date.today().strftime('%Y'))
            mt = int(datetime.date.today().strftime('%m'))
            dt = int(datetime.date.today().strftime('%d'))
            current_date = datetime.date(yr, mt, dt).strftime("%Y%m%d")
            order.order_number = current_date + str(order.id)
            order.save()
            
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }
            
            return render(request, 'orders/payments.html', context)
    
    return redirect('checkout')

def payments(request):
    # Procesar el pago recibido
    body = json.loads(request.body)
    order = Order.objects.get(
        user=request.user, 
        is_ordered=False, 
        order_number=body['orderID']
    )
    
    # Crear registro de pago
    payment = Payment.objects.create(
        user=request.user,
        payment_id=body['transID'],
        payment_method=body['payment_method'],
        amount_paid=order.order_total,
        status=body['status']
    )
    
    # Actualizar orden
    order.payment = payment
    order.is_ordered = True
    order.save()
    
    # Procesar items del carrito
    cart_items = CartItem.objects.filter(user=request.user)
    
    for cart_item in cart_items:
        # Crear producto de orden
        order_product = OrderProduct.objects.create(
            order=order,
            payment=payment,
            user=request.user,
            product=cart_item.product,
            quantity=cart_item.quantity,
            product_price=cart_item.product.price,
            ordered=True
        )
        
        # Agregar variaciones
        order_product.variations.set(cart_item.variation.all())
        
        # Actualizar stock del producto
        product = cart_item.product
        product.stock -= cart_item.quantity
        product.save()
    
    # Limpiar carrito
    cart_items.delete()
    
    # Enviar correo de confirmación
    mail_subject = 'Tu compra fue realizada!'
    body = render_to_string('orders/order_recieved_email.html', {
        'user': request.user,
        'order': order,
    })
    
    send_email = EmailMessage(mail_subject, body, to=[request.user.email])
    send_email.send()
    
    return JsonResponse({
        'order_number': order.order_number,
        'transID': payment.payment_id,
    })

def order_complete(request):
    # Obtener detalles de orden y pago
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
    
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        
        # Calcular subtotal
        subtotal = sum(item.product_price * item.quantity for item in ordered_products)
        
        payment = Payment.objects.get(payment_id=transID)
        
        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }
        
        return render(request, 'orders/order_complete.html', context)
    
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')