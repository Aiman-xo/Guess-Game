from django.contrib import admin
from .models import Customer,Product1,Order,Category

# Register your models here.
admin.site.register(Customer)
admin.site.register(Product1)
admin.site.register(Order)
admin.site.register(Category)