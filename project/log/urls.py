from django.urls import path
from log import views

urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('loginn/',views.loginn,name='loginn'),
    path('logout/',views.logout_view,name='logout'),
    path('activate/<uidb64>/<token>/', views.ActivateAccountView.as_view(), name='activate'),
    path('resetview/',views.reset.as_view(),name='resetview'),
    
    
    
]