from django.urls import path
from product import views

urlpatterns = [
    path('product/',views.product,name='product'),
    path('productview/<int:pk>',views.product_view,name='productview'),
    path('category/<str:ab>',views.category,name='category'),    
]