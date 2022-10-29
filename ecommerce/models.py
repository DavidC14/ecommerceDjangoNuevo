from distutils.command.upload import upload
from email.policy import default
from django.conf import settings
from django.db import models
import os


# Create your models here.
class categorias(models.Model):
    nombre_cat = models.CharField(max_length=50)
    activo = models.BooleanField(default=True)
    def __str__(self) -> str:
            return self.nombre_cat


def marketplace_directory_path(instance, filename):
    banner_pic_name='ecommerce/product/{0}/{1}'.format(instance.name, filename)
    full_path = os.path.join(settings.MEDIA_ROOT, banner_pic_name)
    if os.path.exists(full_path):
        os.remove(full_path)

    return banner_pic_name

class stockProducts(models.Model):
    thumbnail = models.ImageField(blank=True, null=True, upload_to=marketplace_directory_path)
    nom_prod = models.CharField(max_length=50)
    cant_prod = models.IntegerField()
    precio_prod = models.FloatField()   
    descripcion = models.TextField(max_length=250)
    categoria = models.ForeignKey(categorias, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.nom_prod

class carrito(models.Model):
    nom_prod = models.TextField(max_length=200)
    cant_prod = models.IntegerField()
    precio_prod = models.FloatField()
    def __str__(self) -> str:
        return self.nom_prod