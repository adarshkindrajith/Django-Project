from django.urls import path
from home import views

urlpatterns = [
    path('', views.index,name='index'),
    path('about/', views.about,name='about'),
    path('contact/', views.contact,name='contact'),
]