from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product, Variation
from .models import Cart, CartItem
from django.db import transaction
from django.contrib import messages
from decimal import Decimal


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
        tax_rate = Decimal('0.16')  # Convert to Decimal instead of float
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        totals = cart_items.aggregate(
            total=Sum(F('product__price') * F('quantity')),
            quantity=Sum('quantity')
        )
        
        total = totals['total'] or Decimal('0')  # Use Decimal('0') instead of 0
        quantity = totals['quantity'] or 0
        tax = round(tax_rate * total, 2)
        grand_total = total + tax

    except ObjectDoesNotExist:
        total = Decimal('0')  # Use Decimal('0')
        quantity = 0
        tax = Decimal('0')  # Use Decimal('0')
        grand_total = Decimal('0')  # Use Decimal('0')
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
    total = Decimal('0')
    quantity = 0
    tax = Decimal('0')
    grand_total = Decimal('0')
    cart_items = []

    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        if not cart_items:
            messages.warning(request, "Tu carrito está vacío.")
            return redirect('store')

        cart_summary = cart_items.aggregate(
            total=Sum(F('product__price') * F('quantity')),
            quantity=Sum('quantity')
        )
        
        if cart_summary['total']:
            total = cart_summary['total']
            quantity = cart_summary['quantity']
        
        tax = round(Decimal('0.16') * total, 2)  # Use Decimal('0.16') instead of 0.16
        grand_total = total + tax

    except ObjectDoesNotExist:
        messages.error(request, "Hubo un problema al obtener tu carrito.")
        return redirect('store')

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request, 'store/checkout.html', context)

