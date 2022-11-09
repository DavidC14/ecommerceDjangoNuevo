from msilib.schema import Error
import re
from unittest import result
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from .models import stockProducts, carrito, pedidos, categorias
from . import forms
from ecommerce import models
import operator

from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersGetRequest , OrdersCaptureRequest
import sys, json



def paypal(request):
    total = 0
    prods = carrito.objects.all().filter(user = request.user)
    for prod in prods:
        total += prod.precio_prod
    if request.method == "POST":
        pedidos.objects.create(nombre = request.POST['nombre'] + request.POST['apellido'], DNI = request.POST['DNI'], telefono = request.POST['telefono'], total = total)
    return render(request, 'paypal.html',{
        'total':total
    })



# def pago(request):
#     data = json.loads(request.body)
#     order_id = data['orderID']
#     detalle = GetOrder().get_order(order_id)
#     detalle_precio = float (detalle.result.purchase_units[0].amount.value)
#     print(detalle_precio)

#     trx = CaptureOrder().capture_order(order_id, debug=True)
#     pedido = models.Compra(
#         id= trx.result.id,
#         estado= trx.result.status,
#         codigo_estado= trx.status_code,
#         nombre_cliente= trx.result.payer.name.given_name,
#         apellido_cliente= trx.result.payer.name.surname,
#         correo_cliente= trx.result.payer.email_address,
#         direccion_cliente= trx.result.purchase_units[0].shipping.address.address_line_1)
#     pedido.save()
#     data = {
#         "id": f"{trx.result.id}",
#         "nombre_cliente": f"{trx.result.payer.name.given_name}"
#     }
#     return JsonResponse(data)



# class PayPalClient:
#     def __init__(self):
#         self.client_id = "AZEr3NvMIdU0MhJt9Y0GNfb6BTP4FJyCWg6uOrV_QC9SK2QrgZMndjjdVknM-lfA5-J9LeRP4pKvhaCb"
#         self.client_secret = "EJDECmbo4dasEyT4pj2ZwKrFhox1W_PlZ1AI8cQstgi9TkD9KHzUhppOvtS0mOJFOH3y5FLy8QRLd4vA"    
#         self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
#         self.client = PayPalHttpClient(self.environment)
#     def object_to_json(self, json_data):
#         result = {}
#         if sys.version_info[0] < 3:
#             itr = json_data.__dict__.iteritems()
#         else:
#             itr = json_data.__dict__.items()
#         for key,value in itr:
#             if key.startswith("__"):
#                 continue
#             result[key] = self.array_to_json_arrray(value) if isinstance(value, list) else\
#                         self.object_to_json(value) if not self.is_primittive(value) else\
#                             value
#         return result

#     def array_to_json_array(self, json_array):
#         result=[]
#         if isinstance(json_array, list):
#             for item in json_array:
#                 result.append(self.object_to_json(item) if not self.is_primittive(item) \
#                                 else self.array_to_json_array(item) if isinstance(item, list) else item)
#         return result

#     def is_primittive(self, data):
#         return isinstance(data, str) or isinstance(data, unicode) or isinstance(data, int)

# class GetOrder(PayPalClient):
#   def get_order(self, order_id):
#     request = OrdersGetRequest(order_id)
#     response = self.client.execute(request)
#     print('Status Code: ', response.status_code)                    
#     print('Status: ', response.result.status)
#     print ('Order ID: ', response. result.id)              
#     print ('Intent: ', response. result. intent)                  
#     print ('Links:')                                                
#     for link in response.result.links:
#         print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
#         print('Gross Amount: {} {}'.format(response.result.purchase_units[0].amount.currency_code,response.result.purchase_units[0].amount.value))
                        

# class CaptureOrder (PayPalClient):
#    def capture_order(self, order_id, debug=False):
#      request = OrdersCaptureRequest(order_id)
#      response = self.client.execute(request)
#      if debug:
#        print('Status Code: ', response.status_code)
#        print('Status: ', response.result.status)
#        print('Order ID: ', response.result.id)
#        print('Links: ')
#        for link in response.result.links:
#             print('\t{}: {}\tCall Type: {}'.format(link.href, link.method))
#        print('Capture Ids: ')
#        for purchase_unit in response.result.purchase_units:
#             for capture in purchase_unit.payments.captures:
#                 print('\t', capture.id)
#             print("Buyer:")
#             print ("\tEmail Address: {}\n\tName: {}\n\tPhone Number: {}".format(response.result.payer.email_address,
#                 response.result.payer.name.given_name + " " + response.result.payer.name.surname,
#                 response.result.payer.phone.phone_number.national_number))
#             return response


def home(request):
    return render(request, 'home.html')

def aboutus(request):
    return render(request, 'aboutus.html')
    
def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html',{
            'form' : UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                # print(user)
                user.save()
                # print("HASTA ACA LLEGAJAJAJ")
                # login(request, user)
                return redirect('/signin/')
            except:
                
                return render(request, 'signup.html',{
                    'form' : UserCreationForm,
                    'error': 'Usuario existente'
                })
        else:
            return render(request, 'signup.html',{
                'form' : UserCreationForm,
                'error': 'Las contraseñas no coinciden'
            })

@login_required
def signout(request):
    logout(request)
    return redirect('/')


def signin(request):
    if request.method == 'GET':

        return render(request, 'signin.html',{
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:

            return render(request, 'signin.html',{
                'form': AuthenticationForm,
                'error': "El usuario o contraseña es incorrecto"
            })
        else:
            login(request, user)
            return redirect('/buy')
        
    
@login_required
def addStock(request):
  
    if request.method == 'GET':
        return render(request, 'addProduct.html', {
            'form' : forms.stockForm
        })
    else:
        print(request.POST)
        print(models.categorias.objects.get(id=request.POST['categoria']))

        stockProducts.objects.create(thumbnail = request.FILES['thumbnail'], nom_prod=request.POST['nom_prod'], precio_prod=request.POST['precio_prod'], descripcion=request.POST['descripcion'],
        categoria=models.categorias.objects.get(id=request.POST['categoria']))

        return redirect('buy')


@login_required
def buy(request):
    busqueda = request.GET.get("buscar")
      
    stock = stockProducts.objects.all()
    categoria = categorias.objects.all()

    if busqueda:
        stock = stockProducts.objects.filter(
            nom_prod__icontains = busqueda
        )
    
    return render(request, 'buy.html', {
        'products' : stock,
        'categorias':categoria
    })

@login_required 
@staff_member_required
def delete_prod(request, prod):
    
    product = get_object_or_404(stockProducts, nom_prod=prod)
    if request.method == 'POST':
        
        product.delete()
        return redirect('buy')

@login_required
def addCart(request, prod):
    ArrayProductos = []
    cantidad = request.GET.get("cant")


    product = get_object_or_404(stockProducts, nom_prod=prod)
    products = carrito.objects.all().filter(user = request.user)

    for i in products:
        ArrayProductos.append(i.nom_prod)

    if cantidad:
        if product.nom_prod in ArrayProductos:
            p = carrito.objects.filter(user = request.user).get(nom_prod=prod)
            p.cant_prod += int(cantidad)
            p.precio_prod += p.precio_prod*int(cantidad)
            p.save()
        else:
            carrito.objects.create(foto = product.thumbnail, nom_prod = product.nom_prod, cant_prod=int(cantidad), precio_prod = product.precio_prod*int(cantidad), prod = product, user = request.user)
       
    else:
        return render(request, "product_detail.html",{
            'data':product,
            'error': 'No se eligio una cantidad'
        })    
    
    return redirect('cart')



def contacto(request):
    
    if request.method=="POST":
        
        miFormulario=forms.FormularioContacto(request.POST)

        if miFormulario.is_valid():
            inForm=miFormulario.cleaned_data
            print(inForm)
            send_mail(inForm['asunto'], inForm['mensaje'], inForm.get('email', ''), ['davidarechagaippolito@gmail.com'],)

            return render(request, "formulario_contacto.html")
    else:

        miFormulario=forms.FormularioContacto()

    
    
    return render(request, "formulario_contacto.html", {"form":miFormulario})

@login_required
def cart(request):
    total = 0
    prods = carrito.objects.all().filter(user = request.user)
    for prod in prods:
        total += prod.precio_prod
    
    
    return render(request, 'addToCart.html',{
        'prods': prods,
        'total': total
    })

    
@login_required 
def deleteFromCart(request, prod):
 
    product = carrito.objects.filter(user = request.user).get(nom_prod=prod)
    if request.method == 'POST':
        product.delete()
        return redirect('cart')

@login_required
def product_detail(request, id):
    product = stockProducts.objects.get(pk=id)
    return render(request, 'product_detail.html',{
        'data': product
    })

@staff_member_required
def update_stock(request, prod):
    product = get_object_or_404(stockProducts, nom_prod=prod)

    product.hayStock = operator.not_(product.hayStock)
    product.save()
    

    return redirect('buy')

@login_required
def preCompra(request):
    form = forms.preCompra
    return render(request, 'preCompra.html',{
        'form': form
    })


@staff_member_required
@login_required
def verPedidos(request):
    ventas = pedidos.objects.all()
    totalPedidos = pedidos.objects.all().count()
    totalCliente = User.objects.all().count()
    totalGanancia = 0
    for i in ventas:
        totalGanancia += i.total
    return render(request, 'pedidosTotales.html',{
        'pedidos': ventas,
        'total': totalPedidos,
        'totalCliente': totalCliente,
        'ganancia': totalGanancia
    })

@login_required
@staff_member_required
def eliminarPedido(request, pedido):
    venta = pedidos.objects.get(pk = pedido)
    if request.method == 'POST':

        venta.delete()
    return redirect('verPedidos')

@login_required
def delete_all(request):
    prods = carrito.objects.all().filter(user = request.user)
    if request.method == 'POST':
        prods.delete()
        return redirect('cart')

@login_required
def filtrar(request, cat):
    tipo = categorias.objects.get(pk=cat)
    cats = categorias.objects.all()
    
    stock = stockProducts.objects.filter(
        categoria = tipo
    )
    
    return render(request, 'buy.html', {
        'products' : stock,
        'categorias':cats,
    })