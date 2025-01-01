from django.urls import path
from product import views

urlpatterns = [
    path('product/',views.product,name='product'),
    path('productview/<int:pk>',views.product_view,name='productview'),
    path('category/<str:ab>',views.category,name='category'),    
    path('brand/<str:ab>',views.brand,name='brand'), 
    path('profileview/',views.profileview,name='profileview'),
    path('address/',views.address,name='address'),
    path('updateaddress/<int:pk>',views.updateaddress,name='updateaddress'),
    path('deleteaddress/<int:pk>/',views.deleteaddress,name='deleteaddress'),
    path('changepassword/',views.changepassword.as_view(),name='changepassword'),
]