from .import views
from django.urls import path
urlpatterns = [
    path('addtocart/<int:product_id>/',views.addtocart,name='addtocart'),
    path('showcart/',views.showcart,name='showcart'),
    path('checkout/',views.showcart,name='checkout'),
]