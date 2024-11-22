from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserForm, UserProfileForm, CustomSignupForm
from .models import UserProfile
from orders.models import Order
from allauth.account.views import SignupView, LoginView, LogoutView, PasswordResetView
from carts.views import _cart_id
from carts.models import Cart, CartItem

# Vista personalizada de registro utilizando SignupView de django-allauth
class CustomSignupView(SignupView):
    form_class = CustomSignupForm  # Formulario de registro personalizado
    template_name = 'accounts/register.html'  # Plantilla a utilizar para la vista de registro

    # Método para manejar el formulario cuando es válido
    def form_valid(self, form):
        response = super().form_valid(form)
        # Mensaje de éxito después del registro
        messages.success(self.request, 'Te has registrado exitosamente. Por favor verifica tu correo electrónico.')
        return response
    
class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    
    def form_valid(self, form):
        # Primero ejecutamos el form_valid del padre para completar el login
        response = super().form_valid(form)
        
        # En allauth, el usuario ya está autenticado después de super().form_valid()
        user = form.user  # <- Esta es la forma correcta de obtener el usuario en allauth
        
        try:
            # Obtiene el carrito asociado con la sesión actual
            cart = Cart.objects.get(cart_id=_cart_id(self.request))
            is_cart_item_exist = CartItem.objects.filter(cart=cart).exists()
            
            if is_cart_item_exist:
                cart_items = CartItem.objects.filter(cart=cart)
                
                # Obtiene las variaciones de los ítems en el carrito
                product_variation = []
                for item in cart_items:
                    variation = item.variation.all()
                    product_variation.append(list(variation))
                
                # Verifica los ítems existentes en el carrito del usuario
                existing_cart_items = CartItem.objects.filter(user=user)
                ex_var_list = []
                id_list = []
                
                for item in existing_cart_items:
                    existing_variation = item.variation.all()
                    ex_var_list.append(list(existing_variation))
                    id_list.append(item.id)
                
                # Actualiza o crea ítems en el carrito
                for pr in product_variation:
                    if pr in ex_var_list:
                        # Si la variación existe, aumenta la cantidad
                        index = ex_var_list.index(pr)
                        item_id = id_list[index]
                        item = CartItem.objects.get(id=item_id)
                        item.quantity += 1
                        item.user = user
                        item.save()
                    else:
                        # Asigna los ítems del carrito al usuario
                        cart_items = CartItem.objects.filter(cart=cart)
                        for item in cart_items:
                            item.user = user
                            item.save()
        
        except Cart.DoesNotExist:
            pass
        
        messages.success(self.request, 'Has iniciado sesión exitosamente')
        return response

# Vista del panel de usuario, requiere que el usuario esté autenticado
@login_required(login_url='account_login')
def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)  # Obtener órdenes del usuario
    orders_count = orders.count()  # Contar órdenes del usuario
    userprofile = UserProfile.objects.get(user_id=request.user.id)  # Obtener perfil del usuario

    context = {
        'orders_count': orders_count,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/dashboard.html', context)  # Renderizar la plantilla del dashboard con el contexto

# Vista de las órdenes del usuario, requiere que el usuario esté autenticado
@login_required(login_url='account_login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')  # Obtener las órdenes del usuario
    context = {
        'orders': orders,
    }
    return render(request, 'accounts/my_orders.html', context)  # Renderizar la plantilla de las órdenes con el contexto

# Vista para editar el perfil del usuario, requiere que el usuario esté autenticado
@login_required(login_url='account_login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)  # Obtener el perfil del usuario o devolver un 404 si no existe
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()  # Guardar los cambios en el formulario del usuario
            profile_form.save()  # Guardar los cambios en el formulario del perfil
            messages.success(request, 'Su información fue guardada con éxito')  # Mensaje de éxito
            return redirect('edit_profile')  # Redirigir a la misma vista después de guardar
    else:
        user_form = UserForm(instance=request.user)  # Inicializar formulario del usuario con datos actuales
        profile_form = UserProfileForm(instance=userprofile)  # Inicializar formulario del perfil con datos actuales

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/edit_profile.html', context)  # Renderizar la plantilla de edición de perfil con el contexto

# Vista para cambiar la contraseña del usuario, requiere que el usuario esté autenticado
@login_required(login_url='account_login')
def change_password(request):
    # Redirigir a la vista de cambio de contraseña de allauth
    return redirect('account_change_password')
