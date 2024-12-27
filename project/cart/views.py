from django.shortcuts import render,get_object_or_404
from .cart import Cart
from product.models import Product
from django.http import JsonResponse


# Create your views here.

def cart_summary(request):
    return render(request,'cart/cartsum.html',{})

def cart_add(request):
    cart=Cart(request)
    if request.POST.get('action')=='post':
        product_id=int(request.POST.get(product_id))
        product=get_object_or_404(Product,id=product_id)
        cart.add(product=product)

        #get cart quantity
        cart_quantity= cart.__len__()

        #return response
        response=JsonResponse({'qty':cart_quantity})
        return response

def cart_delete(request):
    return render(request,'cart/cartdelete.html')

def cart_update(request):
    return render(request,'cart/cartupdate.html')