
# 🚀 NeonTech E-Commerce

[![Python](https://img.shields.io/badge/Python-3.13.2-336ea0?labelColor=000000\&style=for-the-badge\&logo=python\&logoColor=FFFFFF)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2-092E20?labelColor=000000\&style=for-the-badge\&logo=django\&logoColor=FFFFFF)](https://www.djangoproject.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0.46-bf720d?labelColor=000000\&style=for-the-badge\&logo=mysql\&logoColor=FFFFFF)](https://www.mysql.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS-v%204.0-006fb2?labelColor=000000&style=for-the-badge&logo=tailwindcss&logoColor=ffffff&link=https://tailwindcss.com/)](https://tailwindcss.com/)

**NeonTech** es una plataforma de comercio electrónico robusta desarrollada con **Django**. Aunque está enfocada inicialmente en la venta de laptops y celulares, su arquitectura permite escalar fácilmente a cualquier catálogo de productos. Incluye un sistema completo de gestión de inventario, control de usuarios y procesamiento de órdenes.

![NeonTech E-Commerce Preview](./docs/images/neontech-preview.png)

## ✨ Características

### 🛠 Autenticación y Seguridad

* **Gestión de Usuarios:** Registro de clientes y sistema de login seguro.
* **Roles Definidos:** Diferenciación de permisos entre **Administradores** y **Clientes**.
* **Protección de Datos:** Uso de estándares de seguridad de Django para el manejo de sesiones y contraseñas.

### ⚙️ Panel de Administración (Back-office)

* **Gestión Integral de Inventario (CRUD):**

  * Control total sobre productos con formularios validados para **Creación** y **Edición**.

  * **Sistema de persistencia física:** Lógica personalizada de directorios que organiza los archivos multimedia de cada producto en una estructura clara y mantenible:

    * **Automatización de carpetas:** Al crear un producto, se genera automáticamente una estructura basada en su categoría y nombre (slugificado).

    * **Refactorización dinámica:** Uso de `shutil` para mover archivos físicamente y actualizar rutas en BD ante cambios de nombre o categoría, evitando rutas rotas.

    * **Limpieza de residuos:** Proceso atómico que elimina registros y archivos asociados a un producto para evitar residuos en el sistema.

* **Manejo Avanzado de Media:**

  * **Imagen Principal:** Procesada y renombrada automáticamente como main.jpg para consistencia.

  * **Galería (Carrusel):** Soporte para múltiples imágenes adicionales almacenadas en una subcarpeta dedicada.

    ```plaintext
      media/
      └── productos/
          ├── celulares/
          │   └── {nombre_producto}/
          │       ├── main.jpg              # Imagen principal
          │       └── carrusel/
          │           ├── image1.jpg
          │           ├── image2.jpg
          │           └── image3.jpg
          └── laptops/
              └── {nombre_producto}/
                  ├── main.jpg
                  └── carrusel/
                      ├── image1.jpg
                      ├── image2.jpg
                      └── image3.jpg
    ```

* **Administración de Usuarios y Órdenes:**

  * **Control de Roles:** Gestión de cuentas con permisos diferenciados.

  * **Flujo de Pedidos:** Monitor centralizado con modales de confirmación.

### 🛍️ Interfaz de Cliente

* **Experiencia de Navegación:**

  * **Catálogo Inteligente:** Filtrado por categorías con validación de stock en tiempo real.

  * **Visualización Detallada:** Galería dinámica que consume las imágenes de la carpeta carrusel y ficha técnica del producto.

* **Carrito y Checkout:**

  * Gestión persistente de productos seleccionados con cálculo automático de subtotales e impuestos.

  * **Simulación de Pasarela de Pago:** Validación lógica contra una "Billetera Virtual" en la base de datos.

    * Verificación de saldo suficiente y autenticidad de credenciales.

    * **Proceso Atómico:** Al confirmar el pago, se reduce el stock, se descuenta el saldo del usuario y se genera la orden de compra en un solo flujo.

## 🧰 Tecnologías Utilizadas

* **Base de datos:** MySQL 8.0.46
* **Lenguaje:** Python 3.13.2
* **Framework web:** Django 5.2
* **Estilos:** Tailwind CSS v4.0
* **Control de versiones:** Git

## 📋 Instalación y Configuración Local

**Sigue estos pasos para ejecutar NeonTech en tu máquina local:**

### Requisitos Previos

* Python 3.13.2 instalado
* MySQL 9.2.0 en funcionamiento
* Git instalado
* Gestor de base de datos

### Pasos de Instalación

1. **Clonar el repositorio:**

   ```bash
   git clone https://github.com/tu-usuario/NeonTech.git
   cd NeonTech
   ```

2. **Crear y activar entorno virtual:**
  
    * **Windows (PowerShell):**

      ```powershell
        python -m venv .venv
        .venv\Scripts\Activate.ps1
      ```

    * **Windows (Git Bash):**
  
      ```bash
      python -m venv .venv
      source .venv/Scripts/activate
      ```

    * **Linux/Mac:**

      ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```

3. **Instalar dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configurar variables de entorno:**
  
    * Copia `.env.example` a `.env`:

      ```bash
      cp .env.example .env
      ```

    * Edita `.env` con tu configuración local:

      ```ini
      DEBUG=True
      SECRET_KEY=tu_secret_key_super_segura_aqui
      DATABASE_URL=mysql://usuario:contraseña@127.0.0.1:3306/neontech_db
      ```

5. **Crear base de datos:**

    * Abre tu gestor de base de datos O MySQL CLI y ejecuta con los valores que hayas puesto en `DATABASE_URL`:

      ```sql
        CREATE DATABASE neontech_db;
        CREATE USER 'usuario'@'localhost' IDENTIFIED BY 'contraseña';
        GRANT ALL PRIVILEGES ON neontech_db.* TO 'usuario'@'localhost';
        FLUSH PRIVILEGES;
      ```

6. **Ejecutar migraciones:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

7. **Crear usuario administrador:**

    ```bash
      python manage.py create_admin
    ```

      **O con valores personalizados:**

      ```bash
      python manage.py create_admin \
        --email admin@neontech.com \
        --username admin \
        --password tu_contraseña \
        --firstname Admin \
        --lastname User
      ```

8. **Ejecutar servidor de desarrollo:**

   ```bash
   python manage.py runserver
   ```

    *Haz Ctrl + clic en `http://127.0.0.1:8000/` para abrirlo en tu navegador*.

## 📂 Estructura del Proyecto

```plaintext
NeonTech/
│
├── docs/                        # 📄 Documentación e imágenes del README
│   ├── readme_main.png
│   ├── admin_readme.png
│   └── client_readme.png
│
├── media/                       # 🖼️ Archivos multimedia 
│   └── productos/               # Se genera localmente al subir productos
│       ├── celulares/
│       └── laptops/
│
├── config/                      # ⚙️ Configuración principal de Django
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py              # Configuración del proyecto
│   ├── urls.py                  # URLs principales
│   └── wsgi.py
│
├── core/                        # 🏢 Aplicación principal del comercio
│   │
│   ├── management/              # 🛠️ Comandos personalizados
│   │   └── commands/
│   │       └── create_admin.py  # Comando para crear usuario admin
│   │
│   ├── migrations/              # 🗄️ Migraciones de base de datos
│   │
│   ├── models/                  # 📊 Modelos de datos
│   │   ├── __init__.py
│   │   ├── user.py              # Modelo base de usuario
│   │   ├── admin.py             # Modelos para administrador
│   │   └── client.py            # Modelos para cliente
│   │
│   ├── forms/                   # 📋 Formularios Django
│   │   ├── __init__.py
│   │   ├── admin_forms.py       # Formularios de administrador
│   │   ├── auth_forms.py        # Formularios de autenticación
│   │   └── client_forms.py      # Formularios de cliente
│   │
│   ├── views/                   # 👁️ Lógica de negocio
│   │   ├── __init__.py
│   │   ├── admin_views.py       # Vistas del panel administrador
│   │   ├── auth_views.py        # Vistas de autenticación
│   │   └── client_views.py      # Vistas del cliente
│   │
│   ├── templates/               # 🎨 Plantillas HTML
│   │   └── core/
│   │       ├── start_page.html
│   │       ├── admin_dashboard/
│   │       │   ├── client_form.html
│   │       │   ├── client_management.html
│   │       │   ├── inventory.html
│   │       │   ├── inventory_form.html
│   │       │   ├── orders_management.html
│   │       │   └── partials/
│   │       ├── client_dashboard/
│   │       │   ├── client_dashboard.html
│   │       │   ├── product_description.html
│   │       │   ├── search_products_page.html
│   │       │   ├── shopping_cart.html
│   │       │   ├── shopping_cart_payment.html
│   │       │   └── partials/
│   │       ├── auth/
│   │       │   ├── login_page.html
│   │       │   └── register_page.html
│   │       └── partials/
│   │           └── messages.html
│   │
│   ├── static/                  # 📁 Archivos estáticos
│   │   ├── css/
│   │   │   ├── start_page.css
│   │   │   ├── admin/
│   │   │   ├── auth/
│   │   │   └── client/
│   │   ├── js/
│   │   │   ├── admin/
│   │   │   └── client/
│   │   └── images/
│   │
│   ├── templatetags/            # 🏷️ Tags personalizados
│   │   └── form_filters.py
│   │
│   ├── apps.py
│   ├── urls.py                  # Rutas de la aplicación
│   └── __init__.py
│
├── .env                         # 🔐 Variables de entorno (NO versionado)
├── .env.example                 # 📝 Plantilla de variables de entorno
├── .gitignore                   # 🚫 Archivos ignorados por Git
├── .python-version              # 🐍 Versión de Python del proyecto
├── manage.py                    # ⚙️ Script de administración de Django
├── requirements.txt             # 📦 Dependencias Python
└── README.md                    # 📖 Este archivo
```

## 📷 Capturas de Pantalla

### 🏠 Página de Inicio

*Página de bienvenida con CTA para registro e inicio de sesión.*

![Pagina de Inicio](/docs/images/start_page.png)

### 🔐 Autenticación

*Formularios de registro e inicio de sesión.*

![Autentificación](/docs/images/auth.png)

### 🛠️ Interfaz del administrador

*Gestión de inventario y ordenes.*

![Inventario y órdenes](/docs/images/inventory-and-orders-table.png)

*Gestión de usuarios.*

![Manejo de Clientes](/docs/images/client-table-and-form.png)

### 🛒 Interfaz del cliente

*Interfaz amigable para navegación de productos y compras.*

![Productos y Detalles del Producto](./docs/images/store-product-pages.png)

*Carrito de compras con validación de stock y simulación de pago.*

![Carrito de compras y Pago](./docs/images/shopping-cart-and-payment.png)

## 📝 Convenciones de Commits

Este proyecto sigue [Conventional Commits](https://www.conventionalcommits.org/es/v1.0.0/):

```bash
feat: agregar nueva característica
fix: corregir un bug
docs: cambios en documentación
style: cambios de formato o estilos
refactor: refactorización de código
perf: mejoras de rendimiento
test: agregar o actualizar tests
chore: cambios en herramientas o configuración
```

**Ejemplo:**

```bash
git commit -m "feat: agregar carrito de compras"
git commit -m "fix: corregir error en validación de email"
```

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! He creado Issues para funcionalidades pendientes etiquetadas como good first issue. Si quieres contribuir, puedes tomar uno de esos temas o proponer mejoras mediante un nuevo Issue.

### Flujo para contribuir

1. Haz un Fork del proyecto.
2. Crea una rama de característica (`git checkout -b feature/nombre-caracteristica`).
3. Realiza tus cambios y haz commit siguiendo los estándares mencionados.
4. Sube tus cambios (`git push origin feature/nombre-caracteristica`).
5. Abre un Pull Request describiendo detalladamente tus cambios.
6. Espera la revisión y responde a cualquier comentario o sugerencia.
7. Una vez aprobado, tu PR será fusionado al proyecto principal.

### ✅ Checklist antes de enviar un PR

* [ ] Asegúrate de que no haya conflictos con la rama `main`.
* [ ] Prueba localmente que todas las funcionalidades sigan operativas.
* [ ] Actualiza la documentación si tus cambios lo requieren.
* [ ] Sigue el estilo de código del proyecto.

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver archivo [LICENSE](LICENSE) para más detalles.

## 👤 Autores

| [<img alt="Rosario Cabrera" src="https://github.com/RossCabrera.png" width="50px;"/>](https://github.com/RossCabrera) | [<img alt="Roy Coronado" src="https://github.com/roycvx.png" width="50px;"/>](https://github.com/roycvx) |
| :---: | :---: |
| Rosario Cabrera | Roy Coronado |

---

> *Si te gustó el proyecto, no dudes en darle ⭐ y compartirlo. ¡Gracias por tu apoyo!*

---
