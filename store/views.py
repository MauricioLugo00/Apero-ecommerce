from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import Product, ReviewRating, ProductGallery
from categories.models import Category
from carts.models import CartItem
from carts.views import _cart_id
#from orders.models import OrderProduct
from .forms import ReviewForm

def store(request, category_slug=None):
    """
    Vista para mostrar la tienda con productos filtrados por categoría opcional
    y paginación.
    """
    products = Product.objects.filter(is_available=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Configuración de paginación
    paginator = Paginator(products.order_by('id'), 6)
    page = request.GET.get('page')
    products_paginated = paginator.get_page(page)
    
    context = {
        'products': products_paginated,
        'product_count': products.count(),
    }
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    """
    Vista para mostrar el detalle de un producto específico,
    incluyendo su información, reseñas y galería.
    """
    single_product = get_object_or_404(
        Product,
        category__slug=category_slug,
        slug=product_slug
    )
    
    # Verificar si el producto está en el carrito
    in_cart = CartItem.objects.filter(
        cart__cart_id=_cart_id(request),
        product=single_product
    ).exists()
    
    # Verificar si el usuario ha comprado el producto
    orderproduct = None
    if request.user.is_authenticated:
        orderproduct = OrderProduct.objects.filter(
            user=request.user,
            product=single_product
        ).exists()
    
    # Obtener reseñas y galería del producto
    reviews = ReviewRating.objects.filter(
        product=single_product,
        status=True
    )
    product_gallery = ProductGallery.objects.filter(
        product=single_product
    )
    
    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'orderproduct': orderproduct,
        'reviews': reviews,
        'product_gallery': product_gallery,
    }
    return render(request, 'store/product_detail.html', context)

def search(request):
    """
    Vista para buscar productos por palabra clave en nombre y descripción.
    """
    products = []
    product_count = 0
    keyword = request.GET.get('keyword', '')
    
    if keyword:
        products = Product.objects.filter(
            Q(description__icontains=keyword) |
            Q(product_name__icontains=keyword)
        ).order_by('-created_date')
        product_count = products.count()
    
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)

@require_http_methods(["POST"])
def submit_review(request, product_id):
    """
    Vista para enviar o actualizar una reseña de producto.
    Solo acepta peticiones POST.
    """
    url = request.META.get('HTTP_REFERER')
    
    try:
        # Intentar actualizar una reseña existente
        review = ReviewRating.objects.get(
            user=request.user,
            product_id=product_id
        )
        form = ReviewForm(request.POST, instance=review)
        message = 'Muchas gracias!, tu comentario ha sido actualizado.'
    except ReviewRating.DoesNotExist:
        # Crear una nueva reseña
        form = ReviewForm(request.POST)
        message = 'Muchas gracias!, tu comentario ha sido publicado.'
    
    if form.is_valid():
        if not hasattr(form, 'instance') or not form.instance.pk:
            review = form.save(commit=False)
            review.user = request.user
            review.product_id = product_id
            review.ip = request.META.get('REMOTE_ADDR')
        form.save()
        messages.success(request, message)
    
    return redirect(url)
