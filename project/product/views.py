from django.shortcuts import render,get_object_or_404,redirect
from .models import Product,Category,Brand,Customer
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login
from django.views.generic import View




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
    


def brand(request,ab):
    ab=ab.replace('-',' ')
    try:
        brand=Brand.objects.get(name=ab)
        products=Product.objects.filter(brand=brand)
        return render(request,'product/category.html',{'products':products, 'brand':brand})
    except:
        messages.success(request,("That brand Doesn't Exist..."))
        return redirect('product')
    



#profile view
def profileview(request):
    if request.method=="POST":
        user=request.user
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        location=request.POST['location']
        city=request.POST['city']
        pincode=request.POST['pincode']
        phone=request.POST['phone']

        if user and first_name and last_name and location and city and pincode and phone:
            reg=Customer(user=user,first_name=first_name,last_name=last_name,location=location,city=city,phone=phone,pincode=pincode)
            reg.save()
            messages.success(request,"Profile updated Successfully...!!")
        else:
            messages.error(request, "All fields are required.")
    else:
        messages.warning(request,"Please Set Your Profile")
    return render(request,"profile/profile.html")



def address(request):
    add=Customer.objects.filter(user=request.user)
    return render(request,"profile/address.html",{'add':add})




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
        return redirect('address')  # Redirect to the address page
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
    



