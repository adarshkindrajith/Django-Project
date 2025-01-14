from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control


from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse

from product.models import Product, Category, Brand,Order
from django.contrib import messages
# Create your views here.





@login_required(login_url='loginn')
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def owner(request):
    query = request.GET.get('search', '')
    if query:
        users = User.objects.filter(username__icontains=query) | User.objects.filter(email__icontains=query)
    else:
        users = User.objects.all()

    return render(request, 'owner/owner.html', {'users': users,})






@login_required(login_url='loginn')
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def createuser(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Check if the username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different one.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists. Please choose a different one.')
        else:
            # Create the new user if the username and email are unique
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, 'User created successfully!')
            return HttpResponseRedirect(reverse('owner'))

    return render(request, 'owner/createuser.html')



@login_required(login_url='loginn')
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def update(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.save()
        return HttpResponseRedirect(reverse('owner'))

    return render(request, 'owner/update.html', {'user': user})


@login_required(login_url='loginn')
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def product_list(request):
    query = request.GET.get('search', '')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()
    
    return render(request, 'owner/product_list.html', {'products': products})




@login_required(login_url='loginn')
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def product_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        brand_id = request.POST.get('brand')
        description = request.POST.get('description')
        is_sale = request.POST.get('is_sale') == 'on'
        sale_price = request.POST.get('sale_price') or None
        image = request.FILES.get('image')

        category = get_object_or_404(Category, id=category_id)
        brand = get_object_or_404(Brand, id=brand_id)

        Product.objects.create(
            name=name,
            price=price,
            category=category,
            brand=brand,
            description=description,
            image=image,
            is_sale=is_sale,
            sale_price=sale_price,
        )
        messages.success(request, "Product added successfully!")
        return redirect('product_list')

    categories = Category.objects.all()
    brands = Brand.objects.all()
    return render(request, 'owner/product_add.html', {'categories': categories, 'brands': brands})





@login_required(login_url='loginn')
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def product_edit(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.category = get_object_or_404(Category, id=request.POST.get('category'))
        product.brand = get_object_or_404(Brand, id=request.POST.get('brand'))
        product.description = request.POST.get('description')
        product.is_sale = request.POST.get('is_sale') == 'on'
        product.sale_price = request.POST.get('sale_price') or None
        if 'image' in request.FILES:
            product.image = request.FILES['image']
        product.save()
        messages.success(request, "Product updated successfully!")
        return redirect('product_list')

    categories = Category.objects.all()
    brands = Brand.objects.all()
    return render(request, 'owner/product_add.html', {'product': product, 'categories': categories, 'brands': brands})




def product_delete(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    messages.success(request, "Product deleted successfully!")
    return redirect('product_list')


def block_user(request, user_id):
    user = User.objects.get(id=user_id)
    
    # Check if the user is an admin, if so, prevent blocking
    if user.is_staff:
        return redirect('owner')
    
    # Block the user if not an admin
    user.is_active = False
    user.save()
    return redirect('owner')

def unblock_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = True
    user.save()
    return redirect('owner')













@login_required(login_url='loginn')
def orders(request):
    orders = Order.objects.all()
    STATUS_CHOICES = Order._meta.get_field('order_status').choices
    context = {
        'orders': orders,
        'STATUS_CHOICES': STATUS_CHOICES,
    }
    return render(request, 'owner/orders.html', context)





def update_order_status(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('order_status')
        if new_status:
            order.order_status = new_status
            order.save()
        return redirect('orders')
    



