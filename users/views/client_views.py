from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from datetime import datetime
from django.utils.timezone import now
from decimal import Decimal

from ..models import Producto, Carrito, Direccion, Tarjeta, Compra, DetalleCompra

# Constante para el cálculo de impuestos
ITBMS_RATE = Decimal('0.07')  # 7%

@login_required
def client_dashboard(request):
    """Dashboard principal del cliente"""
    carrito_items = Carrito.objects.filter(usuario=request.user)
    articulos = carrito_items.aggregate(Sum('cantidad'))['cantidad__sum'] or 0

    return render(request, 'users/client_dashboard/client_dashboard.html', {
        'articulos': articulos
    })

def products_list(request, categoria):
    """Mostrar la lista de productos disponibles por categoría"""
    productos = Producto.objects.filter(category=categoria, stock__gt=0)

    carrito_items = Carrito.objects.filter(usuario=request.user)
    articulos = carrito_items.aggregate(Sum('cantidad'))['cantidad__sum'] or 0

    # Usar una sola plantilla para ambas categorías
    return render(request, 'users/client_dashboard/search_products_page.html', {
        'productos': productos,
        'articulos': articulos,
        'categoria': categoria  # Pasar la categoría al template
    })

def show_detail_product(request, producto_id):
    """Mostrar los detalles del producto seleccionado"""
    producto = get_object_or_404(Producto, id=producto_id)
    imagenes = producto.galeria.all()  # gracias al related_name

    carrito = Carrito.objects.filter(usuario=request.user)
    articulos = carrito.aggregate(Sum('cantidad'))['cantidad__sum'] or 0
    
    return render(request, 'users/client_dashboard/product_description.html', {
        'producto': producto,
        'imagenes': imagenes,
        'articulos': articulos
    })

@login_required
def show_shopping_cart(request):
    """Mostrar el carrito de compra"""
    carrito = Carrito.objects.filter(usuario=request.user)
    articulos = carrito.aggregate(Sum('cantidad'))['cantidad__sum'] or 0

    subtotal = sum(Decimal(item.subtotal) for item in carrito)
    impuesto = subtotal * ITBMS_RATE
    total = subtotal + impuesto

    return render(request, 'users/client_dashboard/shopping_cart.html', {
        'carrito': carrito,
        'total': total,
        'subtotal': subtotal,
        'impuesto': impuesto,
        'articulos': articulos
    })

@login_required
def add_to_cart(request, producto_id):
    """Agregar un producto al carrito de compra"""
    if request.method == "POST":
        producto = get_object_or_404(Producto, id=producto_id)
        cantidad = int(request.POST.get("cantidad", 1))

        # Verificar que haya suficiente stock
        if producto.stock < cantidad:
            messages.error(request, "No hay suficiente stock disponible para este producto.")
            return redirect('detail_product', producto_id=producto_id)

        # Verifica si el producto ya está en el carrito del usuario
        item, created = Carrito.objects.get_or_create(
            usuario=request.user,
            producto=producto,
            defaults={'cantidad': cantidad, 'subtotal': producto.price * cantidad}
        )

        if not created:
            if item.cantidad + cantidad > producto.stock:
                messages.error(request, "Has excedido el stock disponible para este producto.")
                return redirect('detail_product', producto_id=producto_id)
            item.cantidad += cantidad
            item.subtotal = item.producto.price * item.cantidad
            item.save()

        messages.success(request, "Producto añadido al carrito")

    return redirect('detail_product', producto_id=producto_id)

@login_required
def update_cart(request, producto_id):
    """Actualizar la cantidad de un producto en el carrito"""
    if request.method == 'POST':
        action = request.POST.get('action')
        item = get_object_or_404(Carrito, usuario=request.user, producto_id=producto_id)

        producto = Producto.objects.get(id=producto_id)
        cantidad_de_producto = int(request.POST.get('cantidad'))

        if action == 'increase' and cantidad_de_producto < producto.stock: # Validar exceso de producto disponible
            item.cantidad += 1
            item.subtotal = item.producto.price * item.cantidad  # Actualizar subtotal
        elif action == 'decrease' and item.cantidad > 1:
            item.cantidad -= 1
            item.subtotal = item.producto.price * item.cantidad  # Actualizar subtotal

        item.save()

    return redirect('shopping_cart')

@login_required
def remove_from_cart(request, producto_id):
    """Eliminar un producto del carrito"""
    item = get_object_or_404(Carrito, usuario=request.user, producto_id=producto_id)
    item.delete()
    return redirect('shopping_cart')

@login_required
def cart_payment(request):
    """Pantalla de pago del carrito de compra"""
    carrito = Carrito.objects.filter(usuario=request.user)

    subtotal = sum(Decimal(item.subtotal) for item in carrito)
    impuesto = subtotal * ITBMS_RATE
    total = subtotal + impuesto

    articulos = sum(item.cantidad for item in carrito)
    
    # Verificar si el usuario tiene tarjeta y dirección
    tiene_tarjeta = Tarjeta.objects.filter(usuario=request.user).exists()
    tiene_direccion = hasattr(request.user, 'direccion')
    
    # Obtener datos si existen
    tarjeta = Tarjeta.objects.filter(usuario=request.user).first() if tiene_tarjeta else None
    direccion = request.user.direccion if tiene_direccion else None

    return render(request, 'users/client_dashboard/shopping_cart_payment.html', {
        'articulos': articulos,
        'total': total,
        'subtotal': subtotal,
        'impuesto': impuesto,
        'tiene_tarjeta': tiene_tarjeta,
        'tiene_direccion': tiene_direccion,
        'tarjeta': tarjeta,
        'direccion': direccion,
    })

def link_card(request):
    """Vincular tarjeta al usuario"""
    msg = "Verifique que sus credenciales sean correctas."
    if request.method == "POST":
        serial_input = request.POST.get('serial')
        cvv_input = request.POST.get('cvv')
        fecha_input = request.POST.get('fecha')
        
        tarjeta = Tarjeta.objects.filter(serial=serial_input).first()
        if tarjeta is None:
            messages.error(request, msg)
            return redirect('cart_payment_now')

        # Verificar si la tarjeta ya está asociada a otro usuario
        if tarjeta.usuario is not None and tarjeta.usuario != request.user:
            messages.error(request, "Esta tarjeta ya está asociada a otro usuario.")
            return redirect('cart_payment_now')

        if tarjeta.cvv != cvv_input:
            messages.error(request, msg)
            return redirect('cart_payment_now')

        try:
            fecha_ingresada = datetime.strptime(fecha_input, "%Y-%m-%d").date()
            mes_input = fecha_ingresada.month
            anio_input = fecha_ingresada.year
        except ValueError:
            messages.error(request, msg)
            return redirect('cart_payment_now')

        hoy = now().date()
        if anio_input < hoy.year or (anio_input == hoy.year and mes_input < hoy.month):
            messages.error(request, "La tarjeta está expirada.")
            return redirect('cart_payment_now')

        mes_real = tarjeta.fecha_expiracion.month
        anio_real = tarjeta.fecha_expiracion.year
        if (mes_input != mes_real) or (anio_input != anio_real):
            messages.error(request, msg)
            return redirect('cart_payment_now')

        tarjeta.usuario = request.user
        tarjeta.save()
        messages.success(request, "¡Tarjeta vinculada correctamente!")
        return redirect('cart_payment_now')

    return render(request, 'users/client_dashboard/shopping_cart.html')

@login_required
def unlink_card(request):
    """Desvincular tarjeta del usuario"""
    if request.method == "POST":
        try:
            tarjeta = Tarjeta.objects.get(usuario=request.user)
            tarjeta.usuario = None
            tarjeta.save()
            messages.success(request, "Tarjeta desvinculada correctamente.")
        except Tarjeta.DoesNotExist:
            messages.error(request, "No tienes una tarjeta vinculada.")
    return redirect('cart_payment_now')

@login_required
def update_address(request):
    """Actualizar dirección existente"""
    if request.method == 'POST':
        calle = request.POST.get('calle')
        telefono = request.POST.get('telefono')
        ciudad = request.POST.get('ciudad')
        provincia = request.POST.get('provincia')
        codigo_postal = request.POST.get('codigo_postal')

        if all([calle, telefono, ciudad, provincia, codigo_postal]):
            try:
                direccion = request.user.direccion
                direccion.calle = calle
                direccion.telefono = telefono
                direccion.ciudad = ciudad
                direccion.provincia = provincia
                direccion.codigo_postal = codigo_postal
                direccion.save()
                messages.success(request, 'Dirección actualizada correctamente.')
            except Direccion.DoesNotExist:
                messages.error(request, 'No tienes una dirección registrada.')
        else:
            messages.error(request, 'Todos los campos son obligatorios.')
    
    return redirect('cart_payment_now')

@login_required
def process_payment(request):
    """Procesar el pago de la compra"""
    usuario = request.user

    try:
        tarjeta = Tarjeta.objects.get(usuario=usuario)
    except Tarjeta.DoesNotExist:
        messages.error(request, "Necesitas vincular una tarjeta antes de pagar.")
        return redirect('cart_payment_now')

    if not hasattr(usuario, 'direccion'):
        messages.error(request, "Necesitas registrar una dirección de envío.")
        return redirect('cart_payment_now')

    carrito_items = Carrito.objects.filter(usuario=usuario)
    if not carrito_items.exists():
        messages.error(request, "Tu carrito está vacío.")
        return redirect('cart_payment_now')

    total = sum(item.subtotal * (1 + ITBMS_RATE) for item in carrito_items)
    total = total.quantize(Decimal('0.01'))

    if tarjeta.saldo < total:
        messages.error(request, "Saldo insuficiente en tu tarjeta. Elimina productos del carrito.")
        return redirect('cart_payment_now')

    compra = Compra.objects.create(
        usuario=usuario,
        fecha=now(),
        total=total
    )

    for item in carrito_items:
        DetalleCompra.objects.create(
            compra=compra,
            producto=item.producto,
            cantidad=item.cantidad,
            precio_unitario=item.producto.price
        )
        item.producto.stock -= item.cantidad
        item.producto.save()

    tarjeta.saldo = tarjeta.saldo - total
    tarjeta.save()

    carrito_items.delete()

    # En lugar de redirigir, renderizamos la misma página con un indicador de éxito
    return render(request, 'users/client_dashboard/shopping_cart_payment.html', {
        'pago_exitoso': True,
        'tiene_tarjeta': True,
        'tiene_direccion': True,
        'total': total,
        'compra': compra  # Añade la compra para obtener el ID
    })

def register_address(request):
    """Guardar dirección de envío"""
    if request.method == 'POST':
        calle = request.POST.get('calle')
        telefono = request.POST.get('telefono')
        ciudad = request.POST.get('ciudad')
        provincia = request.POST.get('provincia')
        codigo_postal = request.POST.get('codigo_postal')

        if all([calle, telefono, ciudad, provincia, codigo_postal]):
            if not hasattr(request.user, 'direccion'):
                Direccion.objects.create(
                    usuario=request.user,
                    calle=calle,
                    telefono=telefono,
                    ciudad=ciudad,
                    provincia=provincia,
                    codigo_postal=codigo_postal,
                )
                messages.success(request, 'Dirección guardada correctamente.')
            else:
                messages.info(request, 'Ya tienes una dirección registrada. Puedes editarla si lo deseas.')
        else:
            messages.error(request, 'Todos los campos son obligatorios.')

        return redirect('cart_payment_now')