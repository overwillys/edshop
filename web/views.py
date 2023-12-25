from django.shortcuts import render, get_object_or_404, redirect

from .models import Categoria, Producto
from .carrito import Cart

# Create your views here.
''' VISTAS PARA CATALOGO DE PRODUCTOS '''
def index(request):

    listaProductos = Producto.objects.all()
    listaCategorias = Categoria.objects.all()
    context = {
        'productos': listaProductos,
        'categorias': listaCategorias
    }



    return render(request, 'index.html', context)

def productosPorCategoria(request, categoria_id):
    '''VISTAS PARA FILTRAR PRODUCTOS POR CATEGORIAS'''
    objCategoria = Categoria.objects.get(pk=categoria_id)
    listaProductos = objCategoria.producto_set.all()

    listaCategorias = Producto.objects.all()

    context = {
        'categoria':listaCategorias,
        'productos':listaProductos
    }
    return render(request, 'index.html', context)

def productosPorNombre(request):
    '''a VISTAS PARA FILTRADO DE PRODUCTOS POR NOMBRE'''
    nombre = request.POST['nombre']

    listaProductos = Producto.objects.filter(nombre__contains=nombre)
    listaCategorias = Categoria.objects.all()

    context = {
        'categorias' : listaCategorias,
        'productos': listaProductos
    }
    return render(request, 'index.html', context)

def productoDetalle(request, producto_id):
    '''VISTA PARA EL DETALLE DE PRODUCTO'''
    objProducto = get_object_or_404(Producto, pk=producto_id)
    #objProducto = Producto.objects.get(pk=producto_id)
    context = {
        'producto': objProducto
    }

    return render(request, 'producto.html', context)


''' VISTAS PARA EL CARRITO DE COMPRAS'''

def carrito(request):
    return render(request, 'carrito.html')

def agregarCarrito(request, producto_id):
    # cuando la cantidad viene del formulario
    if request.method == 'POST':
        cantidad = int(request.POST['cantidad'])
    else:
        cantidad = 1


    objProducto = Producto.objects.get(pk=producto_id)
    carritoProducto = Cart(request)
    carritoProducto.add(objProducto, cantidad)

    #print(request.session.get("carrito"))

    if request.method == 'GET':
        return redirect('/')

    return render(request, 'carrito.html')

def eliminarProductoCarrito(request, producto_id):
    objProducto = Producto.objects.get(pk=producto_id)
    carritoProducto = Cart(request)
    carritoProducto.delete(objProducto)

    return render(request, 'carrito.html' )

def limpiarCarrito(request):
    carritoProducto = Cart(request)
    carritoProducto.clear()

    return render(request, 'carrito.html')