from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.stockProducts)
admin.site.register(models.categorias)
admin.site.register(models.carrito)
admin.site.register(models.pedidos)
# admin.site.register(models.Compra)