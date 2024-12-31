from django.db import models
import datetime
from django.contrib.auth.models import User
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
    pincode=models.IntegerField()
    phone=models.CharField(max_length=10,null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Product(models.Model):
    name=models.CharField(max_length=100)
    price=models.CharField(max_length=20)
    category=models.ForeignKey(Category, on_delete=models.CASCADE,default=1)
    brand=models.ForeignKey(Brand, on_delete=models.CASCADE,default=1)
    description=models.CharField(max_length=500,default='',blank=True,null=True)
    image=models.ImageField(upload_to='static/assets/img/')
    is_sale=models.BooleanField(default=False)
    sale_price=models.CharField(blank=True,max_length=20)


    def __str__(self):
        return self.name


class Order(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    quantity= models.IntegerField(default=1)
    address=models.CharField(max_length=100,default='',blank=True)
    phone=models.CharField(max_length=20,default='',blank=True)
    date=models.DateField(default=datetime.datetime.today)
    status=models.BooleanField(default=False)

    def __str__(self):
        return self.product
