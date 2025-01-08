from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control


from django.http import HttpResponseRedirect
from django.urls import reverse


from product.models import Product, Category, Brand
from django.contrib import messages
# Create your views here.




@login_required
def owner(request):
    query = request.GET.get('search', '')
    if query:
        users = User.objects.filter(username__icontains=query) | User.objects.filter(email__icontains=query)
    else:
        users = User.objects.all()
    
    return render(request, 'owner/owner.html', {'users': users})


@login_required
def createuser(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        User.objects.create_user(username=username, email=email, password=password)
        return HttpResponseRedirect(reverse('owner'))

    return render(request, 'owner/createuser.html')


@login_required
def update(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.save()
        return HttpResponseRedirect(reverse('owner'))

    return render(request, 'owner/update.html', {'user': user})



def delete(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return HttpResponseRedirect(reverse('owner'))   


@login_required
def product_list(request):
    query = request.GET.get('search', '')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()
    
    return render(request, 'owner/product_list.html', {'products': products})



@login_required
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





@login_required
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