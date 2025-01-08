from django.urls import path
from .import views

urlpatterns = [
    path('owner/',views.owner,name='owner'),
    path('owner/create/', views.createuser, name='createuser'),
    path('owner/update/<int:user_id>/', views.update, name='update'),
    path('owner/delete/<int:user_id>/', views.delete, name='delete'),
    
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.product_add, name='product_add'),
    path('products/edit/<int:id>/', views.product_edit, name='product_edit'),
    path('products/delete/<int:id>/', views.product_delete, name='product_delete'),
]