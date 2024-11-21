from .models import Cart, CartItem
from .views import _cart_id
from django.db.models import Sum

# Función para contar la cantidad total de ítems en el carrito
def counter(request):
    cart_count = 0  # Inicializa el contador de ítems en el carrito a 0
    
    try:
        if request.user.is_authenticated:  # Verifica si el usuario ha iniciado sesión
            # Filtra los ítems del carrito del usuario autenticado que están activos y suma la cantidad
            cart_items = CartItem.objects.filter(
                user=request.user, 
                is_active=True
            ).aggregate(total_quantity=Sum('quantity'))
            # Asigna la cantidad total de ítems al contador, si no hay ítems, asigna 0
            cart_count = cart_items['total_quantity'] or 0
        else:
            # Obtiene el carrito del usuario no autenticado usando el ID del carrito
            cart = Cart.objects.filter(cart_id=_cart_id(request)).first()
            if cart:
                # Filtra los ítems del carrito que están activos y suma la cantidad
                cart_items = CartItem.objects.filter(
                    cart=cart, 
                    is_active=True
                ).aggregate(total_quantity=Sum('quantity'))
                # Asigna la cantidad total de ítems al contador, si no hay ítems, asigna 0
                cart_count = cart_items['total_quantity'] or 0
    except Cart.DoesNotExist:
        cart_count = 0  # Si no existe el carrito, el contador de ítems se mantiene en 0
        
    return {'cart_count': cart_count}  # Retorna un diccionario con el conteo de ítems en el carrito
