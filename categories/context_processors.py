from .models import Category

def menu_links(request):
    """
    Recupera todas las categorías para usar en menús de navegación.
    
    Returns:
        dict: Un diccionario con todas las categorías.
    """
    return {'links': Category.objects.all()}