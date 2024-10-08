# Apero: Innovación en cada copa

Apero es un e-commerce desarrollado con Django, que permite a los usuarios comprar bebidas personalizables en vasos únicos. Nuestro sistema facilita la compra de productos personalizados, con un enfoque en la sencillez y la eficiencia tanto para los usuarios como para los administradores.

## ¿En qué consiste?

El proyecto **Apero** utiliza Django como su framework backend, con MySQL como base de datos, y plantillas HTML, CSS, JavaScript y Bootstrap para el frontend. Ofrece una tienda en línea donde los usuarios pueden personalizar vasos para bebidas, gestionar sus compras y acceder a diferentes funcionalidades como administración de cuentas y pedidos.

>[!NOTE]
> El enfoque del proyecto es brindar una experiencia de usuario fácil e intuitiva tanto para clientes como administradores.

---

## Aplicaciones y sus características

- **accounts**: Gestión de usuarios, incluyendo registro, inicio de sesión y manejo de perfiles.
- **carts**: Permite a los usuarios añadir productos a su carrito, actualizar cantidades y proceder al pago.
- **category**: Administra las categorías de productos para facilitar la búsqueda y navegación.
- **ecommerce**: Módulo principal que maneja las vistas relacionadas con la tienda, como el catálogo y las opciones de personalización.
- **orders**: Gestiona los pedidos realizados por los clientes, incluyendo el estado de la compra y el historial de órdenes.
- **store**: Maneja la visualización de productos, integración con las categorías y búsqueda.

>[!CAUTION]
> Mantén las migraciones de la base de datos actualizadas para evitar problemas con la gestión de productos y pedidos.

---

## Uso del administrador en Django

Para acceder a la sección de administración del sistema:

1. Crea un superusuario ejecutando el siguiente comando:
   ```bash
   python manage.py createsuperuser

2. Accede a la URL `localhost:8000/admin` e ingresa las credenciales del superusuario.
Desde esta interfaz de administración, podrás:

- **Gestionar productos**: Agregar, editar o eliminar productos de la tienda.
- **Ver pedidos**: Revisar órdenes, gestionar su estado y verificar la información del cliente.
- **Configurar categorías**: Añadir o modificar categorías de productos.
- **Gestionar usuarios**: Revisar información de las cuentas de usuario y asignar roles o permisos.

>[!TIP] 
> La interfaz de administración de Django es altamente personalizable y permite añadir o quitar opciones de gestión según tus necesidades.

---

## Funcionalidades para los clientes

- **Registro e inicio de sesión**: Los usuarios pueden crear una cuenta con su correo electrónico, verificar su identidad y acceder a todas las funciones del sitio.
- **Personalización de vasos**: Apero permite a los usuarios seleccionar diferentes estilos y diseños de vasos, personalizando su compra.
- **Carrito de compras**: Añadir productos al carrito, ajustar cantidades y proceder al pago de manera sencilla.
- **Gestión de pedidos**: Los usuarios pueden ver el estado de sus órdenes, revisar compras anteriores y gestionar sus datos personales.
- **Proceso de pago seguro**: Integración con sistemas de pago como PayPal y tarjetas de crédito para transacciones rápidas y seguras.

>[!CAUTION] 
> Asegúrate de configurar correctamente las credenciales de pago para garantizar la seguridad en las transacciones.

---

## Autoría

Este proyecto fue desarrollado por **Mauricio Lugo**, **Danells Montes**, **Juan Hoyos**, **Juan Caraballo**, y **Maria Camila**. Si encuentras algún problema o tienes sugerencias para mejorar el sistema, no dudes en ponerte en contacto con nosotros.

¡Gracias por apoyar este proyecto!
