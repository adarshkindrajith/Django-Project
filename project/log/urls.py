from django.urls import path
from log import views 
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('loginn/',views.loginn,name='loginn'),
    path('logout/',views.logout_view,name='logout'),
    path('activate/<uidb64>/<token>/', views.ActivateAccountView.as_view(), name='activate'),


    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='log/reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='log/resetdone.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='log/resetconfirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='log/resetcomplete.html'), name='password_reset_complete'),


]