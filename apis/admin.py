from django.contrib import admin
from .models import Brand, Category, Employee, Customer, CustomerDetail, Shop, ShopDetail, Currency, Invoice, InvoiceItem, Item

# Register your models here.
admin.site.register(Customer)
admin.site.register(Employee)
admin.site.register(CustomerDetail)
admin.site.register(Shop)
admin.site.register(ShopDetail)
admin.site.register(Currency)
admin.site.register(Invoice)
admin.site.register(InvoiceItem)
admin.site.register(Item)