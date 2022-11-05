
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class categorias(models.Model):
    nombre_cat = models.CharField(max_length=50)
    activo = models.BooleanField(default=True)
    def __str__(self) -> str:
            return self.nombre_cat

def marketplace_directory_path():
    return 'productos'

class stockProducts(models.Model):
    thumbnail = models.ImageField(null=True, upload_to=marketplace_directory_path())
    nom_prod = models.CharField(max_length=50)   
    precio_prod = models.FloatField()   
    descripcion = models.TextField(max_length=250)
    categoria = models.ForeignKey(categorias, on_delete=models.CASCADE)
    hayStock = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.nom_prod

class carrito(models.Model):
    foto = models.ImageField(null=True)
    nom_prod = models.TextField(max_length=200)
    cant_prod = models.IntegerField()
    precio_prod = models.FloatField()
    prod = models.ForeignKey(stockProducts, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.nom_prod


class pedidos(models.Model):
    nombre = models.TextField()
    DNI = models.IntegerField()
    telefono = models.IntegerField()
    total = models.FloatField()
    
# class Compra(models.Model):
#     id = models.CharField(primary_key= True, max_length=100)
#     estado = models.CharField(max_length=100, null=True)
#     codigo_estado = models.CharField(max_length=100, null=True)
#     # producto = models.ForeignKey(to=carrito, on_delete= models.SET_NULL, null = True),
#     total_de_la_compra= models.DecimalField(max_digits=5 ,decimal_places=2, null=True)
#     nombre_cliente = models.CharField(max_length=100, null=True)
#     apellido_cliente=models.CharField(max_length=100, null=True)
#     correo_cliente = models.EmailField(max_length=100, null=True)
#     direccion_cliente = models.CharField(max_length=100, null=True)
#     def _str_(self):
#         return self.nombre_cliente