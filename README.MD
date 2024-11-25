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
- **core**: Módulo principal que maneja las vistas relacionadas con la tienda, como el catálogo y las opciones de personalización.
- **orders**: Gestiona los pedidos realizados por los clientes, incluyendo el estado de la compra y el historial de órdenes.
- **store**: Maneja la visualización de productos, integración con las categorías y búsqueda.

>[!IMPORTANT]
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

Este proyecto fue desarrollado por **Mauricio Lugo**. Si encuentras algún problema o tienes sugerencias para mejorar el sistema, no dudes en ponerte en contacto con nosotros.

¡Gracias por apoyar este proyecto!

>[!NOTE]
> SECCION PARA LOS DESARROLLADORES DE LA WEB
## Modo desarrollo

Esta sección está destinada solo para el equipo de desarrollo de Apero. A continuación se describen las aplicaciones del proyecto y sus funcionalidades.

1. **Accounts**:
   Esta aplicación generalmente se encarga de todo lo relacionado con los usuarios.
   **Funcionalidades comunes**:
   - Registro y autenticación de usuarios.
   - Login/logout y gestión de sesiones.
   - Perfiles de usuario (donde los usuarios pueden ver y modificar su información).
   - Recuperación de contraseñas.
   - Permisos y roles para gestionar lo que los usuarios pueden hacer en el sistema (administradores, clientes, etc.).

2. **Store**:
   Esta aplicación suele ser el corazón del ecommerce, ya que se encarga de la gestión de los productos que están a la venta en la tienda.
   **Funcionalidades comunes**:
   - Gestión del catálogo de productos.
   - Visualización de detalles de productos (nombre, precio, descripción, imágenes).
   - Filtrado y búsqueda de productos.
   - Promociones y descuentos.
   - Inventario (control de stock de productos).

3. **Category**:
   Esta aplicación es crucial para la organización de los productos. Permite que los productos se agrupen en diferentes categorías.
   **Funcionalidades comunes**:
   - Creación de categorías (como bebidas alcohólicas, vinos, cervezas, etc.).
   - Asignación de productos a categorías.
   - Posibilidad de filtrar productos por categoría en el frontend del sitio web.
   - Puede incluir subcategorías para una mejor organización.

4. **Carts**:
   Esta aplicación gestiona el carrito de compras de los usuarios.
   **Funcionalidades comunes**:
   - Agregar, eliminar o modificar productos en el carrito.
   - Guardar el estado del carrito para usuarios autenticados y no autenticados (a través de cookies o sesiones).
   - Resumen del carrito, mostrando el total, impuestos y descuentos aplicados.
   - Actualizar cantidades de productos.
   - Pasar a la compra (checkout), donde el carrito se convierte en una orden.

6. **Orders**:
   Esta aplicación gestiona todo lo relacionado con las órdenes de compra.
   **Funcionalidades comunes**:
   - Crear y guardar órdenes cuando el usuario finaliza el checkout.
   - Historial de órdenes (los usuarios pueden ver sus compras pasadas).
   - Actualizar el estado de las órdenes (pendiente, pagada, enviada, entregada).
   - Puede incluir facturación o detalles de pagos.

7. **Static**:
   La carpeta static es el lugar donde se almacenan los archivos estáticos del proyecto, que son archivos que no cambian según las interacciones del usuario.
   **Archivos comunes en static**:
   - CSS: para los estilos del sitio.
   - JavaScript: para la funcionalidad interactiva del frontend.
   - Imágenes: logos, banners u otras imágenes que forman parte del diseño del sitio.
   Estos archivos son servidos directamente al navegador del usuario sin pasar por el servidor de Django.

8. **Templates**:
   La carpeta templates contiene los archivos HTML que se usan para la renderización del sitio web.
   **Funcionalidades comunes**:
   - Diseño y estructura de páginas: home, productos, categorías, carrito, checkout, etc.
   - Integración de Django Template Language (DTL), lo que permite renderizar datos dinámicos desde el backend de Django (por ejemplo, mostrar productos desde la base de datos).
   - Los archivos HTML suelen incluir includes (como la cabecera y el pie de página) y bloques de código reutilizables.

9. **Otros elementos en el proyecto**:
   - **manage.py**: Este archivo es el comando de administración de Django. A través de él, puedes correr comandos como runserver, migrate, createsuperuser, entre otros.
   - **requirements.txt**: Este archivo lista todas las dependencias del proyecto, es decir, los paquetes Python que necesitas instalar (incluyendo Django).



