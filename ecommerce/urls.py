
from django.urls import path, include
from . import views

from django.views.generic import TemplateView

urlpatterns = [
    path('', views.home, name="home"),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('addStock/', views.addStock, name='addStock'),
    path('buy', views.buy, name="buy"),
    path('buy/<str:prod>/delete', views.delete_prod, name='delete_prod'),
    path('cart/', views.cart, name="cart"),
    path('cart/delete_all', views.delete_all, name="delete_all"),
    path('cart/<str:prod>', views.addCart, name="addCart"),
    path('cart/delete/<str:prod>', views.deleteFromCart, name="deleteFromCart"),
    path('cart/update/<str:prod>', views.update_stock, name="update_stock"),
    path('contacto/', views.contacto, name="contacto"),
    path('aboutus/', views.aboutus, name="aboutus"),
    path('product/<int:id>', views.product_detail, name="product_detail"),
    path('paypal/', views.paypal, name="paypal"),
    path('preCompra/', views.preCompra, name="preCompra"),
    path('datos/', views.verPedidos, name="verPedidos"),
    path('datos/delete/<int:pedido>', views.eliminarPedido, name="eliminarPedido"),
    path('filtrar/<int:cat>', views.filtrar, name="filtrar"),
    # path('pago/', views.pago, name="pago")

]

