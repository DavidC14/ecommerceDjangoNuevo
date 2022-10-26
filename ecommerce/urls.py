
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('addStock/', views.addStock, name='addStock'),
    path('buy/', views.buy, name="buy"),
    path('buy/<str:prod>/delete', views.delete_prod, name='delete_prod'),
    path('carrito/', views.cart, name="cart"),
    path('carrito/<int:prod>', views.addCart, name="addCart"),
    path('contacto/', views.contacto, name="contacto"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)