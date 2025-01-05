from .import views
from django.urls import path
urlpatterns = [
    path('addtocart/<int:product_id>/',views.addtocart,name='addtocart'),
    path('showcart/',views.showcart,name='showcart'),
    path('checkout/',views.showcart,name='checkout'),
    path('plus-cart/',views.plus_cart,name='plus-cart'),
    path('minus-cart/', views.minus_cart, name='minus_cart'),
    path('remove-cart/', views.remove_cart, name='remove_cart'),
    
]