# Trabajo practico final - Proyecto Informatico II
## Bagual Django E-commerce
- Facundo Arechaga
- David Chajade
- Julian Ippolito

### Se trata de un e-commerce que ofrece y vende bolsos, carteras, riñoneras y otros productos. Esta desarrollado con el framework Backend de Python llamado Django. Y diseñado con HTML y CSS.
#### Se necesitan instalar las siguientes librerias:
- `pip install django`
- `pip install paypal-checkout-serversdk`
- `pip install django-allauth`
#### Puesta en marcha: 
- `python manage.py runserver`
#### Funcionalidades del e-commerce:
- Iniciar sesion
- Registrarse
- Enviar mensaje de contacto por email
- Ver productos
- Agregar producto al carrito y seleccionar cantidad
- Filtrar productos o buscar en la barra de busqueda
- Vaciar carrito y eliminar producto del carrito
- Comprar productos
#### Usando cuenta de administrador:
- Agregar producto
- Borrar producto
- Ver pedidos
- Eliminar pedidos
- Visualizar datos de pedido (cantidad de usuarios, ganancias totales, etc)
- Eliminar stock momentaneamente

## Requerimientos
![image](https://user-images.githubusercontent.com/104697921/200146824-959e4955-843f-4ec2-aa82-58de2eb91f9d.png)
#### El punto 5) no se llego a completar por falta de tiempo. Se logro incluir el metodo de pago mediante paypal, el cual permite pagar con el dinero de la cuenta, o utilizando una tarjeta externa.

## Modelo relacional
![der](https://user-images.githubusercontent.com/104697921/200147027-26060409-4187-4bee-81ae-34c126cf6433.png)

## RoadMap
### Se podrian agregar mas funcionalidades, como:
- Editar productos 
- Integrar de mejor manera en el backend el formato de pago con paypal para que cuando se efectue la transaccion, los datos de la misma se almacenen en la base de datos.
- Poder añadir mas imagenes a un producto
- Agregar mas informacion a los productos
