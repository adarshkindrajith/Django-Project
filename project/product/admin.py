from django.contrib import admin
from .models import Category,Product,Customer,Order,Brand

# Register your models here.
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)