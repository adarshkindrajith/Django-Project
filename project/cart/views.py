from django.shortcuts import render,redirect, get_object_or_404
from .models import Cart
from product.models import Product,Order,Customer,Payment
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages


from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
# Create your views here.





@login_required(login_url='loginn')
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def addtocart(request, product_id):
    user = request.user
    product = get_object_or_404(Product, id=product_id)
    

    cart_item = Cart.objects.filter(user=user, product=product).first()
    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:

        Cart.objects.create(user=user, product=product, quantity=1) 
    return redirect('product')








@login_required(login_url='loginn')
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def showcart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    total_amount = sum(
        (item.product.sale_price if item.product.is_sale and item.product.sale_price else item.product.price) * item.quantity
        for item in cart
    )
    shipping_cost = 40  
    total_with_shipping = total_amount + shipping_cost

    context = {
        'cart': cart,
        'amount': total_amount,
        'totalamount': total_with_shipping,
    }
    return render(request, 'cart/addtocart.html', context)



def plus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        try:
            cart_item = Cart.objects.get(Q(product_id=prod_id) & Q(user=request.user))
            cart_item.quantity += 1
            cart_item.save()

            # Recalculate the total amount and total with shipping
            user = request.user
            cart = Cart.objects.filter(user=user)
            total_amount = sum(
                (item.product.sale_price if item.product.is_sale and item.product.sale_price else item.product.price) * item.quantity
                for item in cart
            )
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
            total_amount = sum(
                (item.product.sale_price if item.product.is_sale and item.product.sale_price else item.product.price) * item.quantity
                for item in cart
            )
            shipping_cost = 40 if cart.exists() else 0  # Set shipping to 0 if cart is empty
            total_with_shipping = total_amount + shipping_cost

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
            cart_item = Cart.objects.get(Q(product_id=prod_id) & Q(user=request.user))
            cart_item.delete()

            user = request.user
            cart = Cart.objects.filter(user=user)
            total_amount = sum(
                (item.product.sale_price if item.product.is_sale and item.product.sale_price else item.product.price) * item.quantity
                for item in cart
            )
            shipping_cost = 40 if cart.exists() else 0  # Set shipping to 0 if cart is empty
            total_with_shipping = total_amount + shipping_cost

            data = {
                'amount': total_amount,
                'total_amount': total_with_shipping,
                'action': 'deleted',
                'cart_empty': not cart.exists(),
            }
            return JsonResponse(data)
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Cart item not found'}, status=404)






@login_required(login_url='loginn')
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def checkout(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)

    total_amount = sum(
        (item.product.sale_price if item.product.is_sale and item.product.sale_price else item.product.price) * item.quantity
        for item in cart_items
    )
    shipping_cost = 40
    total_with_shipping = total_amount + shipping_cost

    addresses = Customer.objects.filter(user=user)

    if request.method == "POST":
        address_id = request.POST.get('custid')
        payment_method = request.POST.get('payment_method')

        if not address_id:
            messages.error(request, "Please select a shipping address.")
            return redirect('checkout')

        try:
            address = Customer.objects.get(id=address_id, user=user)
        except Customer.DoesNotExist:
            messages.error(request, "Invalid address selected.")
            return redirect('checkout')
    
        if payment_method == "cod":
            # Process COD order
            payment = Payment.objects.create(
                user=user,
                amount=total_with_shipping,
                stripe_payment_status="Pending",  # Mark as pending for COD
                paid=False  # COD is not a paid method at the moment of order creation
            )

            # Create orders for each cart item
            for item in cart_items:
                Order.objects.create(
                    user=user,
                    product=item.product,
                    quantity=item.quantity,
                    customer=address,
                    address=f"{address.location}, {address.city}, {address.pincode}",
                    phone=address.phone,
                    total_amount=total_with_shipping // len(cart_items),  # Divide total among cart items
                    order_status="Placed (Cash On Delivery)",
                    payment=payment,
                )

            cart_items.delete()
            messages.success(request, "Order placed successfully with Cash on Delivery.")
            return redirect('order_summary')

        elif payment_method == "online":
            # Store address ID in session for online payment
            request.session['address_id'] = address.id
            return redirect('stripe_payment')

        else:
            messages.error(request, "Invalid payment method selected.")
            return redirect('checkout')

    context = {
        'cart_items': cart_items,
        'total_amount': total_with_shipping,
        'add': addresses,
    }
    return render(request, 'cart/checkout.html', context)




@login_required(login_url='loginn')
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def order_summary(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-date')

    context = {
        'orders': orders
    }
    return render(request, 'cart/order_summary.html', context)








import stripe
from django.conf import settings
stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required(login_url='loginn')
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def stripe_payment(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)

    # Calculate total amount
    total_amount = sum(
        (item.product.sale_price if item.product.is_sale and item.product.sale_price else item.product.price) * item.quantity
        for item in cart_items
    )
    shipping_cost = 40
    total_with_shipping = total_amount + shipping_cost  # Total amount in INR
    stripe_amount = total_with_shipping * 100  # Stripe requires amounts in cents

    address_id = request.session.get('address_id')
    if not address_id:
        messages.error(request, "Shipping address not found. Please try again.")
        return redirect('checkout')

    try:
        address = Customer.objects.get(id=address_id)
    except Customer.DoesNotExist:
        messages.error(request, "Invalid shipping address.")
        return redirect('checkout')

    if request.method == "POST":
        payment_method_id = request.POST.get("payment_method_id")
        try:
            # Create Stripe Payment Intent
            intent = stripe.PaymentIntent.create(
                amount=stripe_amount,
                currency="inr",
                payment_method=payment_method_id,
                confirmation_method="manual",
                confirm=True,  # Confirm the payment intent immediately
                return_url="http://127.0.0.1:8000/payment_success/",
            )

            # Save payment details
            payment = Payment.objects.create(
                user=user,
                amount=total_with_shipping,
                stripe_payment_intent_id=intent['id'],
                stripe_payment_status="Paid",  # Mark as Paid if successful
                paid=True
            )

            # Create orders and clear the cart
            for item in cart_items:
                Order.objects.create(
                    user=user,
                    product=item.product,
                    quantity=item.quantity,
                    customer=address,
                    address=f"{address.location}, {address.city}, {address.pincode}",
                    phone=address.phone,
                    total_amount=total_with_shipping // len(cart_items),  # Divide total among cart items
                    order_status="Placed",
                    payment=payment,
                )

            cart_items.delete()
            request.session.pop('address_id', None)  # Clear session data
            messages.success(request, "Payment successful! Order placed.")
            return redirect('order_summary')

        except stripe.error.CardError as e:
            # Payment failed; mark payment as pending
            Payment.objects.create(
                user=user,
                amount=total_with_shipping,
                stripe_payment_status="Pending",
                paid=False
            )
            messages.error(request, f"Payment failed: {e.error.message}")
            return redirect('checkout')

    context = {
        'cart_items': cart_items,
        'total_amount': total_with_shipping,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, 'cart/stripe_payment.html', context)
