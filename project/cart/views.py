from django.shortcuts import render,redirect
from .models import Cart
from product.models import Product

# Create your views here.
def addtocart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')



def showcart(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    return render(request,"cart/addtocart.html")