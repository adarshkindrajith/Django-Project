from .import views
from django.urls import path
urlpatterns = [
    path('addtocart/<int:product_id>/',views.addtocart,name='addtocart'),
    path('showcart/',views.showcart,name='showcart'),
    path('plus-cart/',views.plus_cart,name='plus-cart'),
    path('minus-cart/', views.minus_cart, name='minus_cart'),
    path('remove-cart/', views.remove_cart, name='remove_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_summary/', views.order_summary, name='order_summary'),
    path('stripe_payment/', views.stripe_payment, name='stripe_payment'),
]