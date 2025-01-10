from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import CASCADE

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name




class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    location=models.CharField(max_length=200,null=True, blank=True)
    city=models.CharField(max_length=200)
    pincode=models.IntegerField(null=True, blank=True)
    phone=models.CharField(max_length=10,null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Product(models.Model):
    name=models.CharField(max_length=100)
    price = models.IntegerField(null=True, blank=True)
    category=models.ForeignKey(Category, on_delete=models.CASCADE,default=1)
    brand=models.ForeignKey(Brand, on_delete=models.CASCADE,default=1)
    description=models.CharField(max_length=500,default='',blank=True,null=True)
    image=models.ImageField(upload_to='static/assets/img/')
    is_sale=models.BooleanField(default=False)
    sale_price=models.IntegerField(null=True, blank=True)


    def __str__(self):
        return self.name



class Payment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    amount=models.IntegerField()
    razorpay_order_id=models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_status=models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id=models.CharField(max_length=100,blank=True,null=True)
    paid=models.BooleanField(default=False)







STATUS_CHOICES=(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On the way','on the way'),
    ('Deliverd','Deliverd '),
    ('Cancel','Cancel'),
    ('Pending','Pending'),
)



class Order(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, default='', blank=True)
    phone = models.CharField(max_length=20, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    payment = models.ForeignKey(
        'Payment',  # Reference the Payment model
        on_delete=models.CASCADE,
        null=True,  # Allow null values
        blank=True  # Allow blank values in forms
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Order #{self.id} - {self.product.name}"



class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, related_name="wishlist")
    product = models.ForeignKey(Product, on_delete=CASCADE, related_name="wishlisted_by")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f'{self.user.username} - {self.product.name}'
