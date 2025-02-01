from django.contrib import admin
from .models import Category,Customer,Order,Brand,Product
from .models import CarouselImage
# Register your models here.
admin.site.register(Category)
admin.site.register(Brand)




@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','location','city','pincode','phone']



@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display=[ 'id','user','customer','product','quantity','date','phone','address','order_status','cancellation_requested','payment' ]


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display=[ 'name','price','category','brand','description','image','is_sale','sale_price']


@admin.register(CarouselImage)
class CarouselImageAdmin(admin.ModelAdmin):
    list_display = ['image']