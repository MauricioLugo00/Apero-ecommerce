from django.contrib import admin
from . import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta para el panel de administración
    path('', views.home, name='home'),  # Ruta para la página de inicio
    # Incluir URLs de la app accounts
    path('accounts/', include('accounts.urls')),
    # Incluir URLs de allauth para autenticación
    path('accounts/', include('allauth.urls')),
    path('carts/', include('carts.urls')),  # Incluir URLs de la app carts
    path('store/', include('store.urls')),  # Incluir URLs de la app store
    path('orders/', include('orders.urls')), 
]

if settings.DEBUG:
    # Configuración para servir archivos estáticos en modo debug
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
