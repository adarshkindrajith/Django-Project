from django.shortcuts import render,redirect, get_object_or_404
from .models import Cart
from product.models import Product,Order,Customer
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages

# Create your views here.

def addtocart(request, product_id):
    user = request.user
    product = get_object_or_404(Product, id=product_id)
    

    cart_item = Cart.objects.filter(user=user, product=product).first()
    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:

        Cart.objects.create(user=user, product=product, quantity=1) 
    return redirect('showcart')


def showcart(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    total_amount = sum(item.product.price * item.quantity for item in cart)
    shipping_cost = 40  
    total_with_shipping = total_amount + shipping_cost

    context = {
        'cart': cart,
        'amount': total_amount,
        'totalamount': total_with_shipping,
    }
    return render(request,'cart/addtocart.html',context)

def plus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        try:
            cart_item = Cart.objects.get(Q(product_id=prod_id) & Q(user=request.user))
            cart_item.quantity += 1
            cart_item.save()

            user = request.user
            cart = Cart.objects.filter(user=user)
            total_amount = sum(item.product.price * item.quantity for item in cart)
            shipping_cost = 40  # Static shipping cost
            total_with_shipping = total_amount + shipping_cost

            data = {
                'quantity': cart_item.quantity,
                'amount': total_amount,
                'total_amount': total_with_shipping,
            }
            return JsonResponse(data)
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Cart item not found'}, status=404)

def minus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        try:
            # Retrieve the cart item
            cart_item = Cart.objects.get(Q(product_id=prod_id) & Q(user=request.user))

            # Decrement quantity or remove item
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
                action = "updated"
            else:
                cart_item.delete()
                action = "deleted"

            # Recalculate totals
            user = request.user
            cart = Cart.objects.filter(user=user)
            total_amount = sum(item.product.price * item.quantity for item in cart)
            shipping_cost = 40 if cart.exists() else 0  # Set shipping to 0 if cart is empty
            total_with_shipping = total_amount + shipping_cost

            # Prepare response data
            data = {
                'quantity': cart_item.quantity if action == "updated" else 0,
                'amount': total_amount,
                'total_amount': total_with_shipping,
                'action': action,
            }
            return JsonResponse(data)
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Cart item not found'}, status=404)

def remove_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        try:
            # Retrieve and delete the cart item
            cart_item = Cart.objects.get(Q(product_id=prod_id) & Q(user=request.user))
            cart_item.delete()

            # Recalculate totals after removal
            user = request.user
            cart = Cart.objects.filter(user=user)
            total_amount = sum(item.product.price * item.quantity for item in cart)
            shipping_cost = 40 if cart.exists() else 0  # Set shipping to 0 if cart is empty
            total_with_shipping = total_amount + shipping_cost

            # Prepare response data
            data = {
                'amount': total_amount,
                'total_amount': total_with_shipping,
                'action': 'deleted',
                'cart_empty': not cart.exists(),  # Check if the cart is empty
            }
            return JsonResponse(data)
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Cart item not found'}, status=404)








def checkout(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    total_amount = sum(item.product.price * item.quantity for item in cart_items)
    shipping_cost = 40
    total_with_shipping = total_amount + shipping_cost

    addresses = Customer.objects.filter(user=user)

    if request.method == "POST":
        address_id = request.POST.get('custid')
        if not address_id:
            messages.error(request, "Please select a shipping address.")
            return redirect('checkout')

        try:
            address = Customer.objects.get(id=address_id, user=user)
        except Customer.DoesNotExist:
            messages.error(request, "Invalid address selected.")
            return redirect('checkout')

        # Save the order
        for item in cart_items:
            Order.objects.create(
                user=user,
                product=item.product,
                quantity=item.quantity,
                address=address,
                total_amount=total_with_shipping
            )

        # Clear the cart after order placement
        cart_items.delete()
        messages.success(request, "Order placed successfully!")
        return redirect('order_summary')

    context = {
        'cart_items': cart_items,
        'total_amount': total_with_shipping,
        'add': addresses,
    }
    return render(request, 'cart/checkout.html', context)

def order_summary(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')

    context = {
        'orders': orders
    }
    return render(request, 'cart/order_summary.html', context)