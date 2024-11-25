from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.contrib import messages
from decimal import Decimal
from django.template.loader import render_to_string
from django.conf import settings


import datetime
import json

from carts.models import CartItem
from store.models import Product
from .models import Order, Payment, OrderProduct
from .forms import OrderForm

def place_order(request):
    total = 0 
    quantity = 0
    current_user = request.user
    
    cart_items = CartItem.objects.filter(user=current_user)
    
    if cart_items.count() <= 0:
        return redirect('store')
    
    for cart_item in cart_items:
        if cart_item.quantity > cart_item.product.stock:
            messages.error(request, f"Stock insuficiente para {cart_item.product.product_name}")
            return redirect('cart')
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    
    tax = round(Decimal('0.16') * total, 2)
    grand_total = total + tax
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        
        form = OrderForm(request.POST)
        
        if form.is_valid():
            order = form.save(commit=False)
            order.user = current_user
            order.order_total = grand_total
            order.tax = tax
            order.ip = request.META.get('REMOTE_ADDR')
            order.save()
            
            yr = int(datetime.date.today().strftime('%Y'))
            mt = int(datetime.date.today().strftime('%m'))
            dt = int(datetime.date.today().strftime('%d'))
            current_date = datetime.date(yr, mt, dt).strftime("%Y%m%d")
            order.order_number = current_date + str(order.id)
            order.save()
            
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': str(total).replace(',', '.'),  # Aseguramos formato con punto
                'tax': str(tax).replace(',', '.'),      # Aseguramos formato con punto
                'grand_total': str(grand_total).replace(',', '.'),  # Aseguramos formato con punto
                'PAYPAL_CLIENT_ID': settings.PAYPAL_CLIENT_ID, 
            }
            
            return render(request, 'orders/payments.html', context)
    
    return redirect('checkout')


def payments(request):
    # Verificar el método de solicitud
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
        
    # Manejar la decodificación del JSON
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    
    try:
        # Obtener la orden correspondiente
        order = Order.objects.get(
            user=request.user, 
            is_ordered=False, 
            order_number=body['orderID']
        )
        
        # Crear un registro de pago
        payment = Payment.objects.create(
            user=request.user,
            payment_id=body['transID'],
            payment_method=body['payment_method'],
            amount_paid=order.order_total,
            status=body['status']
        )
        
        # Actualizar la orden
        order.payment = payment
        order.is_ordered = True
        order.save()
        
        # Procesar los items del carrito
        cart_items = CartItem.objects.filter(user=request.user)
        
        for cart_item in cart_items:
            # Crear productos de la orden
            order_product = OrderProduct.objects.create(
                order=order,
                payment=payment,
                user=request.user,
                product=cart_item.product,
                quantity=cart_item.quantity,
                product_price=cart_item.product.price,
                ordered=True
            )
            order_product.variations.set(cart_item.variation.all())
            
            # Actualizar el stock del producto
            product = cart_item.product
            product.stock -= cart_item.quantity
            product.save()
        
        # Limpiar el carrito
        cart_items.delete()
        
        # Enviar un correo de confirmación de compra
        mail_subject = 'Tu compra fue realizada!'
        body = render_to_string('orders/order_recieved_email.html', {
            'user': request.user,
            'order': order,
        })
        
        try:
            send_email = EmailMessage(mail_subject, body, to=[request.user.email])
            send_email.send()
        except Exception as e:
            print(f"Error al enviar email: {str(e)}")
        
        # Responder con los detalles de la orden y transacción
        return JsonResponse({
            'order_number': order.order_number,
            'transID': payment.payment_id,
        })
    
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Orden no encontrada'}, status=404)
    except Exception as e:
        print(f"Error al procesar el pago: {str(e)}")
        return JsonResponse({'error': 'Error interno del servidor'}, status=500)

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
            'PAYPAL_CLIENT_ID': settings.PAYPAL_CLIENT_ID, 

        }
        
        return render(request, 'orders/order_complete.html', context)
    
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')