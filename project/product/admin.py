from django.contrib import admin
from .models import Category,Product,Customer,Order,Brand

# Register your models here.
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Order)



@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','location','city','pincode','phone']