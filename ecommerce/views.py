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



def paypal(request):
    total = 0
    prods = carrito.objects.all()
    for prod in prods:
        total += prod.precio_prod
    if request.method == "POST":
        pedidos.objects.create(nombre = request.POST['nombre'] + request.POST['apellido'], DNI = request.POST['DNI'], telefono = request.POST['telefono'], total = total)
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
        return redirect('/')

@login_required
def addCart(request, prod):
    ArrayProductos = []
    cantidad = request.GET.get("cant")


    product = get_object_or_404(stockProducts, nom_prod=prod)
    products = carrito.objects.all()

    for i in products:
        ArrayProductos.append(i.nom_prod)

    if cantidad:
        if product.nom_prod in ArrayProductos:
            p = carrito.objects.get(nom_prod=prod)
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

            send_mail(inForm['asunto'], inForm['mensaje'], inForm.get('email', ''), ['davidarechagaippolito@gmail.com'],)

            return render(request, "buy.html")
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
    return redirect('/')

@login_required
def delete_all(request):
    prods = carrito.objects.all()
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