from django.shortcuts import render,redirect, get_object_or_404
from .models import Cart
from product.models import Product

# Create your views here.
def addtocart(request,product_id):
    user=request.user
    product = get_object_or_404(Product, id=product_id)
    # Add product to cart
    Cart.objects.create(user=user, product=product)
    return redirect('showcart')



def showcart(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    total_amount = sum(item.product.price * item.quantity for item in cart)
    shipping_cost = 40  # Fixed shipping cost
    total_with_shipping = total_amount + shipping_cost

    context = {
        'cart': cart,
        'amount': total_amount,
        'totalamount': total_with_shipping,
    }
    return render(request,'cart/addtocart.html',context)
