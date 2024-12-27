from django.shortcuts import render,get_object_or_404,redirect
from .models import Product,Category
from django.contrib import messages

# Create your views here.
def product(request):
    products=Product.objects.all()
    return render(request,'product/product.html',{'products':products})


def product_view(request,pk):
    product=get_object_or_404(Product, pk=pk)
    return render(request,'product/productview.html',{'product':product})


def category(request,ab):
    ab=ab.replace('-',' ')
    try:
        category=Category.objects.get(name=ab)
        products=Product.objects.filter(category=category)
        return render(request,'product/category.html',{'products':products, 'category':category})
    except:
        messages.success(request,("That category Doesn't Exist..."))
        return redirect('product')