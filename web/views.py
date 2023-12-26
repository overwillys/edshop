from django.shortcuts import render, get_object_or_404, redirect

from .models import Categoria, Producto, Cliente
from .carrito import Cart
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .forms import ClienteForm

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

'''VISTAS PARA CLIENTES Y USUARIOS '''

def crearUsuario(request):
    if request.method == 'POST':
        dataUsuario = request.POST['nuevoUsuario']
        dataPassword = request.POST['nuevoPassword']

        nuevoUsuario = User.objects.create_user(username=dataUsuario, password=dataPassword)
        #verificamos que el usuario se cree correctamente y no sea vacio
        #guardaria los datos de sesion de usuario por medio de la funcion login
        if nuevoUsuario is not None:
            login(request, nuevoUsuario)
            return redirect('/cuenta')#al loguear, redireciona        
    return render(request, 'login.html')

def loginUsuario(request):

    #capturamos el "next q viene por get"

    paginaDestino = request.GET.get('next', None)
    context = {
        'destino': paginaDestino,
    }

    if request.method == 'POST':
        dataUsuario = request.POST['usuario']# lo q me viene del formulario login
        dataPassword = request.POST['password']
        dataDestino = request.POST['destino']

        #lo qviene por request
        usuarioAuth = authenticate(request, username=dataUsuario, password=dataPassword)

        if usuarioAuth is not None:#si que existe hjabrá un objeto
            login(request, usuarioAuth)# se loguea

            if dataDestino != 'None':
                return redirect(dataDestino)


            return redirect('/cuenta')
        else:# y si el usuario no existe
            context = {
                'mensajeError': 'Datos Incorrectos'
            }

    return render(request, 'login.html', context)


def logoutUsuario(request):
    logout(request)
    return render(request, 'login.html')


def cuentaUsuario(request):

    try:
    #le pasamos el usuario logueado si es que existe
        clienteEditar = Cliente.objects.get(usuario = request.user)
        
        #datos del request cuadno hciisemos el login
        dataCliente = {

            'nombre': request.user.first_name,
            'apellidos': request.user.last_name,
            'email':request.user.email,
            'direccion':clienteEditar.direccion,
            'telefono':clienteEditar.telefono,
            'dni':clienteEditar.dni,
            'sexo':clienteEditar.sexo,
            'fecha_nacimiento':clienteEditar.fecha_nacimiento
        }
    except: #datos que siempre van a venir si me logue con usuario q no tiene cliente
        dataCliente = {
        'nombre': request.user.first_name,
        'apellidos': request.user.last_name,
        'email':request.user.email
        }

    frmCliente = ClienteForm(dataCliente) # Creo un objeto de cliente formulario
    context = {     # se lo enviamos a contexto
        'frmCliente': frmCliente
    }

    return render(request, 'cuenta.html', context)

def actualizarCliente(request):
    mensaje = ""
#Todo lo q envie por post, le voy asignar a clienteForm
    if request.method == 'POST':
        frmCliente = ClienteForm(request.POST)
        if frmCliente.is_valid():
            dataCliente = frmCliente.cleaned_data # prepara para poder guardar en la DB

            #actualizar usuario
            actUsuario = User.objects.get(pk=request.user.id)
            actUsuario.first_name = dataCliente["nombre"] # estos viene del formulario
            actUsuario.last_name = dataCliente["apellidos"]
            actUsuario.email = dataCliente["email"]
            actUsuario.save()

            #registrar al cliente
            nuevoCliente = Cliente()
            nuevoCliente.usuario = actUsuario
            nuevoCliente.dni = dataCliente["dni"]
            nuevoCliente.direccion = dataCliente["direccion"]
            nuevoCliente.telefono = dataCliente["telefono"]
            nuevoCliente.sexo = dataCliente["sexo"]
            nuevoCliente.fecha_nacimiento = dataCliente["fecha_nacimiento"]
            nuevoCliente.save()

            mensaje = "Datos Actualizados" # estos mensajes hay q enviarlos al context

    context = {
        'mensaje': mensaje,
        'frmcliente': frmCliente
    }        

    return render(request, 'cuenta.html', context)

'''VISTA PARA EL PROCESO DE COMPRA'''

#usamos el decorador para que vaya a login antes de registrar un pedido
@login_required(login_url='/login')
def registrarPedido(request):
        try:
        #le pasamos el usuario logueado si es que existe
            clienteEditar = Cliente.objects.get(usuario = request.user)
            
            #datos del request cuadno hciisemos el login
            dataCliente = {

                'nombre': request.user.first_name,
                'apellidos': request.user.last_name,
                'email':request.user.email,
                'direccion':clienteEditar.direccion,
                'telefono':clienteEditar.telefono,
                'dni':clienteEditar.dni,
                'sexo':clienteEditar.sexo,
                'fecha_nacimiento':clienteEditar.fecha_nacimiento
            }
        except: #datos que siempre van a venir si me logue con usuario q no tiene cliente
                dataCliente = {

                'nombre': request.user.first_name,
                'apellidos': request.user.last_name,
                'email':request.user.email

            }


        frmCliente = ClienteForm(dataCliente) # Creo un objeto de cliente formulario
        context = {     # se lo enviamos a contexto
            'frmCliente': frmCliente
        }

        return render(request, 'pedido.html', context)