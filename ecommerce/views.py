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
from .models import stockProducts, carrito
from . import forms
from ecommerce import models
import operator
# from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
# from paypalcheckoutsdk.orders import OrdersGetRequest , OrdersCaptureRequest
#import sys




# def pago(request):
#     pass

# class PayPalClient:
#     def __init__(self):
#         self.client_id = "AVuJsj71tA1V4cwBpLWi1t8KSlZVZ6xy3RLOwWcHPYqoZR7UYT4M24II899EoqDKOmSnV4GN53OvuauP"
#         self.client_secret = "EKpyYcKu54VJ5nlhQqOD1rJv60o4e2rh0BJo_MPqShr7H1kTO2lHPfP96tSOCvM4jaJ5alcnxWtkidzn"    
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
#     # print('Status Code: ', response.status_code)                    
#     # print('Status: ', response.result.status)
#     # print ('Order ID: ', response. result.id)              
#     # print ('Intent: ', response. result. intent)                  
#     # print ('Links:')                                                
#     # for link in response.result.links:
#     #   print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
#     # print('Gross Amount: {} {}'.format(response.result.purchase_units[0].amount.currency_code,
#     #                     response.result.purchase_units[0].amount.value))
# if __name__ == '__main__':
#     GetOrder().get_order('REPLACE-WITH-VALID-ORDER-ID')

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
#             # print ("\tEmail Address: {}\n\tName: {}\n\tPhone Number: {}".format(response.result.payer.email_address,
#             #     response.result.payer.name.given_name + " " + response.result.payer.name.surname,
#             #     response.result.payer.phone.phone_number.national_number))
#             return response

# if __name__ == "__main__":
#     order_id = 'REPLACE-WITH-APPORVED-ORDER-ID'
#     CaptureOrder().capture_order(order_id, debug=True)



def paypal(request):
    total = 0

    prods = carrito.objects.all()
    for prod in prods:
        total += prod.precio_prod
    return render(request, 'paypal.html',{
        'total':total
    })

def home(request):
    return render(request, 'home.html')
    
def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html',{
            'form' : UserCreationForm
        })
    else: 
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('/')
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
            return redirect('/')
        
    
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
  

    if busqueda:
        stock = stockProducts.objects.filter(
            nom_prod__icontains = busqueda
        )
    
    return render(request, 'buy.html', {
        'products' : stock
    })

@login_required 
@staff_member_required
def delete_prod(request, prod):
    
    product = get_object_or_404(stockProducts, nom_prod=prod)
    if request.method == 'POST':
        
        product.delete()
        return redirect('/')

@login_required
def addCart(request, prod):
    ArrayProductos = []
    cantidad = request.GET.get("cant")
    product = get_object_or_404(stockProducts, nom_prod=prod)
    products = carrito.objects.all()
    print(product)
    print(products)
    for i in products:
        ArrayProductos.append(i.nom_prod)

    if cantidad:
        if product.nom_prod in ArrayProductos:
            p = carrito.objects.get(nom_prod=prod)
            p.cant_prod += int(cantidad)
            p.precio_prod += p.precio_prod*int(cantidad)
            p.save()
        else:
            carrito.objects.create(nom_prod = product.nom_prod, cant_prod=int(cantidad), precio_prod = product.precio_prod*int(cantidad))
       
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

            send_mail(inForm['asunto'], inForm['mensaje'], inForm.get('email', ''), ['davidarechagaippolito@gmail.com'],)

            return render(request, "buy.html")
    else:

        miFormulario=forms.FormularioContacto()

    
    
    return render(request, "formulario_contacto.html", {"form":miFormulario})

@login_required
def cart(request):
    total = 0
    prods = carrito.objects.all()
    for prod in prods:
        total += prod.precio_prod
    
    
    return render(request, 'addToCart.html',{
        'prods': prods,
        'total': total
    })

    
@login_required 
@staff_member_required
def deleteFromCart(request, prod):
    
    product = get_object_or_404(carrito, nom_prod=prod)
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
