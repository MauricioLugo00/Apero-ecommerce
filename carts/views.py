from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product, Variation
from .models import Cart, CartItem
from django.db import transaction
from django.contrib import messages

# Función para obtener el ID del carrito desde la sesión
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

# Función para agregar un producto al carrito
@transaction.atomic
def add_cart(request, product_id):
    current_user = request.user
    product = get_object_or_404(Product, id=product_id)
    
    # Obtener variaciones del producto
    product_variation = []
    if request.method == 'POST':
        for key, value in request.POST.items():
            try:
                variation = Variation.objects.get(
                    product=product,
                    variation_category__iexact=key,
                    variation_value__iexact=value
                )
                product_variation.append(variation)
            except Variation.DoesNotExist:
                continue

    if current_user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(
            product=product,
            user=current_user,
            defaults={'quantity': 0}
        )
        
        if not created:
            existing_variations = cart_item.variation.all()
            if set(product_variation) == set(existing_variations):
                cart_item.quantity = F('quantity') + 1
                cart_item.save()
                return redirect('cart')
        
        cart_item.quantity = 1
        cart_item.save()
        if product_variation:
            cart_item.variation.clear()
            cart_item.variation.add(*product_variation)
            
    else:
        cart, _ = Cart.objects.get_or_create(cart_id=_cart_id(request))
        cart_item, created = CartItem.objects.get_or_create(
            product=product,
            cart=cart,
            defaults={'quantity': 1}
        )
        
        if not created:
            existing_variations = cart_item.variation.all()
            if set(product_variation) == set(existing_variations):
                cart_item.quantity = F('quantity') + 1
                cart_item.save()
                return redirect('cart')
            
        if product_variation:
            cart_item.variation.clear()
            cart_item.variation.add(*product_variation)

    return redirect('cart')

# Función para remover un producto del carrito
@transaction.atomic
def remove_cart(request, product_id, cart_item_id):
    cart_item = get_object_or_404(
        CartItem,
        product_id=product_id,
        id=cart_item_id,
        user=request.user if request.user.is_authenticated else None,
        cart__cart_id=_cart_id(request) if not request.user.is_authenticated else None
    )
    
    if cart_item.quantity > 1:
        cart_item.quantity = F('quantity') - 1
        cart_item.save()
    else:
        cart_item.delete()
    
    return redirect('cart')

# Función para eliminar un ítem del carrito
def remove_cart_item(request, product_id, cart_item_id):
    cart_item = get_object_or_404(
        CartItem,
        product_id=product_id,
        id=cart_item_id,
        user=request.user if request.user.is_authenticated else None,
        cart__cart_id=_cart_id(request) if not request.user.is_authenticated else None
    )
    cart_item.delete()
    return redirect('cart')

# Función para mostrar el contenido del carrito
def cart(request):
    try:
        tax_rate = 0.16  # 16%
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        totals = cart_items.aggregate(
            total=Sum(F('product__price') * F('quantity')),
            quantity=Sum('quantity')
        )
        
        total = totals['total'] or 0
        quantity = totals['quantity'] or 0
        tax = round(tax_rate * total, 2)
        grand_total = total + tax

    except ObjectDoesNotExist:
        total = quantity = tax = grand_total = 0
        cart_items = []

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request, 'store/cart.html', context)

# Función para realizar el checkout
@login_required(login_url='login')
def checkout(request):
    total = 0
    quantity = 0
    tax = 0
    grand_total = 0
    cart_items = []

    try:
        # Si el usuario está autenticado, usamos su carrito
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            # Para usuarios no autenticados, se utiliza el carrito basado en session
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        # Si no hay elementos en el carrito, mostramos un mensaje de advertencia o redirigimos
        if not cart_items:
            messages.warning(request, "Tu carrito está vacío.")
            return redirect('store')  # O cualquier vista de tu elección.

        # Utilizamos `aggregate()` para calcular `total` y `quantity` de manera más eficiente
        cart_summary = cart_items.aggregate(
            total=Sum(F('product__price') * F('quantity')),  # Cálculo del total
            quantity=Sum('quantity')  # Sumar todas las cantidades
        )
        
        # Si hay resultados, actualizamos las variables
        if cart_summary['total']:
            total = cart_summary['total']
            quantity = cart_summary['quantity']
        
        # Calculamos el impuesto (en este caso, 16%)
        tax = round(0.16 * total, 2)
        grand_total = total + tax

    except ObjectDoesNotExist:
        messages.error(request, "Hubo un problema al obtener tu carrito.")
        return redirect('store')  # Redirigir si el carrito no se encuentra.

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request, 'store/checkout.html', context)

