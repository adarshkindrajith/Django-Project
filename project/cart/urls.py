from django.urls import path
from cart import views

urlpatterns = [
    path(' ',views.cart_summary,name='cart_summary'),
    path('add/',views.cart_add,name='cart-add'),
    path('delete/',views.cart_summary,name='cart_delete'),
    path('update/',views.cart_summary,name='cart_update'),
]