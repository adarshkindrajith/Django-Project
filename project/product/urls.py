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
    path('search/',views.search,name='search'),
    path('logout/',views.logout_view,name='logout'),


    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='addtowishlist'),
    path('remove_from_wishlist/<int:product_id>/', views.remove_from_wishlist, name='removefromwishlist'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    
]