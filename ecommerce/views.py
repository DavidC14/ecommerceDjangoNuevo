from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import stockProducts, carrito
from . import forms
from ecommerce import models
import operator
# Create your views here.

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
    cantidad = request.GET.get("cant")
    product = get_object_or_404(stockProducts, nom_prod=prod)
   
    if cantidad:
        # if product in products:    
            carrito.objects.create(nom_prod = product.nom_prod, cant_prod=int(cantidad), precio_prod = product.precio_prod*int(cantidad))
        # else:
        #     prod = carrito.objects.get(pk=prod)
        #     print('jajajaj' + prod)
        #     prod.cant_prod += int(cantidad)
        #     prod.save()
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


# Falta:
# 1. cambiar como se pone cantidad a comprar
# 2. No poder agregar un mismo producto al carrito