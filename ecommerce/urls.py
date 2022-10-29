
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('addStock/', views.addStock, name='addStock'),
    path('', views.buy, name="buy"),
    path('<str:prod>/delete', views.delete_prod, name='delete_prod'),
    path('carrito/', views.cart, name="cart"),
    path('carrito/<int:prod>', views.addCart, name="addCart"),
    path('carrito/delete/<str:prod>', views.deleteFromCart, name="deleteFromCart"),
    path('contacto/', views.contacto, name="contacto"),
    path('product/<int:id>', views.product_detail, name="product_detail")

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)