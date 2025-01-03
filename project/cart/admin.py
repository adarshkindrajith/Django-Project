from django.contrib import admin
from .models import Cart
# Register your models here.
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display=['id','user','product','quantity']
