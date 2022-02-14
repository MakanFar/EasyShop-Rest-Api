from datetime import date
from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Currency(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=3) 

    def __str__(self) -> str:
        return super().__str__()

class Shop(models.Model):
    name = models.CharField(max_length=20)
    default_currency = models.ForeignKey(Currency, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return super().__str__()

class ShopDetail(models.Model):
    shop = models.OneToOneField(Shop, on_delete=models.CASCADE, related_name='shop_details')
    address = models.CharField(max_length=255)
    zip = models.CharField(max_length=8)
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    commerce = models.CharField(max_length=200)
    logo = models.IntegerField()

    def __str__(self) -> str:
        return super().__str__()


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='shop_employees')

    def __str__(self) -> str:
        return super().__str__()



class Customer(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    shop = models.ForeignKey(Shop, related_name='shop_customers', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return super().__str__()


class CustomerDetail(models.Model):
    customer = models.OneToOneField(Customer, related_name='customer_details', on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    zip = models.CharField(max_length=8)
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)

    def __str__(self) -> str:
        return super().__str__()

class Category(models.Model):
    name = models.CharField(max_length=50)
    shop = models.ForeignKey(Shop, related_name='shop_cats', on_delete=models.CASCADE)


    def __str__(self) -> str:
        return super().__str__()


class Brand(models.Model):
    name = models.CharField(max_length=50)
    shop = models.ForeignKey(Shop, related_name='shop_brands', on_delete=models.CASCADE)


    def __str__(self) -> str:
        return super().__str__()


class Invoice(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_invoices')
    reference = models.CharField(max_length=35)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return super().__str__()

class Item(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True,null=True)
    default_price = models.DecimalField(decimal_places=2, max_digits=20)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True,null=True, related_name='cat_items')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, blank=True,null=True, related_name='brand_items')
    shop = models.ForeignKey(Shop, on_delete=models.PROTECT, related_name='shop_items')

    def __str__(self) -> str:
        return super().__str__()


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='invoice_invoice_items', on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    amount = models.IntegerField()
    item = models.ForeignKey(Item, related_name='item_invoice_items', on_delete=models.PROTECT)

    def __str__(self) -> str:
        return super().__str__()




class InvoicePaid(models.Model):
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)

    def __str__(self) -> str:
        return super().__str__()
