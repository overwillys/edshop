from django.shortcuts import render, get_object_or_404

from .models import Categoria, Producto

# Create your views here.
''' VISTAS PARA CATALOGO DE PRODUCTOS '''
def index(request):

    listaProductos = Producto.objects.all()
    listaCategorias = Categoria.objects.all()
    print(listaCategorias)
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