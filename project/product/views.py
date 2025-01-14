from django.shortcuts import render,get_object_or_404,redirect
from .models import Product,Category,Brand,Customer
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login,logout
from django.views.generic import View
from django.db.models import Q
from .models import CarouselImage


from .models import Wishlist
# Create your views here.
def product(request):
    query = request.GET.get('search', '')
    category_id = request.GET.get('category')
    brand_id = request.GET.get('brand')
    price_filter = request.GET.get('price')

    # Filter by search query
    products = Product.objects.filter(name__icontains=query)

    # Filter by category if selected
    if category_id:
        products = products.filter(category__id=category_id)

    # Filter by brand if selected
    if brand_id:
        products = products.filter(brand__id=brand_id)

    # Filter by price if selected
    if price_filter == 'low':
        products = products.order_by('price')
    elif price_filter == 'high':
        products = products.order_by('-price')

    if not products:
        messages.info(request, "No products found...")
    
    # Get all categories and brands for the filter options
    categories = Category.objects.all()
    brands = Brand.objects.all()
    carousel_images = CarouselImage.objects.all()

    return render(request, 'product/product.html', {
        'carousel_images': carousel_images,
        'products': products,
        'categories': categories,
        'brands': brands,
    })



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
    


def brand(request,ab):
    ab=ab.replace('-',' ')
    try:
        brand=Brand.objects.get(name=ab)
        products=Product.objects.filter(brand=brand)
        return render(request,'product/category.html',{'products':products, 'brand':brand})
    except:
        messages.success(request,("That brand Doesn't Exist..."))
        return redirect('product')
    



@login_required(login_url='loginn')
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
# Profile view
def profileview(request):
    if request.method == "POST":
        user = request.user
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        location = request.POST.get('location')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        phone = request.POST.get('phone')

        # Check if all fields are present
        if user and first_name and last_name and location and city and pincode and phone:
            # Validate that pincode is numeric
            if not pincode.isdigit():
                messages.error(request, "Invalid pincode: must be numeric.")
                return render(request, "profile/profile.html")

            # Validate that phone is numeric and has exactly 10 digits
            if not phone.isdigit() or len(phone) != 10:
                messages.error(request, "Invalid phone number and must be 10-digit ")
                return render(request, "profile/profile.html")

            # Create and save the customer object
            reg = Customer(
                user=user,
                first_name=first_name,
                last_name=last_name,
                location=location,
                city=city,
                phone=phone,
                pincode=int(pincode)  # Convert pincode to an integer
            )
            reg.save()
            messages.success(request, "Profile updated Successfully...!!")
        else:
            messages.error(request, "All fields are required.")
    else:
        messages.warning(request, "Please Set Your Profile")
    
    return render(request, "profile/profile.html")




@login_required(login_url='loginn')
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def address(request):
    add=Customer.objects.filter(user=request.user)
    return render(request,"profile/address.html",{'add':add})




@login_required(login_url='loginn')
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def updateaddress(request,pk):
    add = Customer.objects.get(pk=pk)

    if request.method == "POST":
        # Update fields with the submitted data
        add.first_name = request.POST.get('first_name', add.first_name)
        add.last_name = request.POST.get('last_name', add.last_name)
        add.location = request.POST.get('location', add.location)
        add.city = request.POST.get('city', add.city)
        add.pincode = request.POST.get('pincode', add.pincode)
        add.phone = request.POST.get('phone', add.phone)

        # Save updated object
        add.save()
        messages.success(request, "Congratulations! Profile updated successfully.")
        return redirect('address')  # Redirect to the address page

    # For GET request, render the update form with existing data
    return render(request, "profile/updateaddress.html", {"add": add})
    


def deleteaddress(request, pk):
    add = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        add.delete()
        messages.success(request, "Address deleted successfully.")
        return redirect('address')  #Redirect to the address page
    return redirect('address')





class changepassword(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'profile/changepassword.html')

    @method_decorator(login_required)
    def post(self, request):
        current_password = request.POST['oldpass']
        new_password = request.POST['newpass']
        confirm_new_password = request.POST['confpass']

        # Verify current password
        if not check_password(current_password, request.user.password):
            messages.error(request, "Current password is incorrect.")
            return redirect('changepassword')

        # Verify new passwords match
        if new_password != confirm_new_password:
            messages.error(request, "New passwords do not match.")
            return redirect('changepassword')

        # Update password
        user = request.user
        user.set_password(new_password)
        user.save()

        # Automatically log the user back in after password change
        login(request, user)
        messages.success(request, "Password updated successfully.")
        return redirect('changepassword')  # Redirect to a profile or any desired page
    


def search(request):
    query = request.GET.get('q', '')  # Get the search term from the URL query parameters
    products = Product.objects.filter(name__icontains=query)  # Filter products based on the search term

    return render(request, 'product/search.html', {'products': products, 'query': query})






@login_required(login_url='loginn')
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def logout_view(request):
    logout(request)
    messages.success(request, "Logout successfully")
    return redirect('loginn')




@login_required(login_url='loginn')
def add_to_wishlist(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if the user is not logged in
    
    product = get_object_or_404(Product, id=product_id)

    # Check if the product is already in the user's wishlist
    if Wishlist.objects.filter(user=request.user, product=product).exists():
        # Product is already in the wishlist
        return redirect('product')  # Redirect to the wishlist page

    # Add product to the user's wishlist
    Wishlist.objects.create(user=request.user, product=product)
    return redirect('product')  # Redirect to wishlist page after adding




def remove_from_wishlist(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if the user is not logged in
    
    product = get_object_or_404(Product, id=product_id)
    wishlist_item = Wishlist.objects.filter(user=request.user, product=product).first()

    if wishlist_item:
        wishlist_item.delete()  # Remove product from wishlist
    return redirect('wishlist')  # Redirect to the wishlist page



@login_required(login_url='loginn')
def wishlist_view(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if the user is not logged in

    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'product/wishlist.html', {'wishlist_items': wishlist_items})