from django.urls import path
from .import views

urlpatterns = [
    path('owner/',views.owner,name='owner'),
    path('owner/create/', views.createuser, name='createuser'),
    path('owner/update/<int:user_id>/', views.update, name='update'),
    path('block_user/<int:user_id>/', views.block_user, name='block_user'),
    path('unblock_user/<int:user_id>/', views.unblock_user, name='unblock_user'),
    
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.product_add, name='product_add'),
    path('products/edit/<int:id>/', views.product_edit, name='product_edit'),
    path('products/delete/<int:id>/', views.product_delete, name='product_delete'),


    
]