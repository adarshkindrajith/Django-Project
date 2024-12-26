from django.shortcuts import render
from .models import Product

# Create your views here.
def product(request):
    products=Product.objects.all()
    return render(request,'product/product.html',{'products':products})