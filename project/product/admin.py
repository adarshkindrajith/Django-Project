from django.contrib import admin
from .models import Category,Customer,Order,Brand,Payment

# Register your models here.
admin.site.register(Category)
admin.site.register(Brand)




@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','location','city','pincode','phone']



@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display=[ 'id','user','amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid' ]


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display=[ 'id','user','customer','product','quantity','date','phone','status','payment' ]


