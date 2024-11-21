from django.contrib import admin
from . import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta para el panel de administración
    path('', views.home, name='home'),  # Ruta para la página de inicio
    path('accounts/', include('accounts.urls')),  # Incluir URLs de la app accounts
    path('accounts/', include('allauth.urls')),  # Incluir URLs de allauth para autenticación
    path('carts/', include('carts.urls')),  # Incluir URLs de la app carts
    path('store/', include('store.urls')),  # Incluir URLs de la app store
    # path('categories/', include('categories.urls')),  # Descomentar si decides habilitar la app categories
    # path('orders/', include('orders.urls')),  # Descomentar si decides habilitar la app orders
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Configuración para servir archivos estáticos en modo debug
