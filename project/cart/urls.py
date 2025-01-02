from django.urls import path
from cart import views

urlpatterns = [
    path('addtocart/',views.addtocart,name='addtocart'),
    path('showcart/',views.showcart,name='showcart'),
    
]