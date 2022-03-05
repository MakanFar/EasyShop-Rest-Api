from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class CustomerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerDetail
        fields = ('address', 'zip', 'city', 'country', 'email', 'phone',)


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['name', 'description', 'default_price', 'category', 'brand']

    def create(self, validated_data):
        item = self.Meta.model.objects.create(shop=self.context['request'].user.employee.shop, **validated_data)

        return item


class InvoiceItemSerializer(serializers.ModelSerializer):

    item = serializers.HyperlinkedRelatedField(read_only=True, view_name="apis:item-detail")
    

    class Meta:
        model = InvoiceItem
        fields = ['price', 'amount', 'item']



class InvoiceSerializer(serializers.ModelSerializer):

    invoice_invoice_items = InvoiceItemSerializer(many=True)
    total = serializers.SerializerMethodField(method_name='get_total_price')
    profit = serializers.SerializerMethodField(method_name='get_profit')
    expense = serializers.SerializerMethodField(method_name='get_expense')


    class Meta:
        model = Invoice
        fields = ['reference', 'customer', 'invoice_invoice_items', 'total', 'profit', 'expense']

    def get_total_price(self, instance):
        items = InvoiceItem.objects.filter(invoice=instance)
        total = 0

        for item_item in items:
            total += item_item.price * item_item.amount
        return total

    def get_profit(self, instance):
        items = InvoiceItem.objects.filter(invoice=instance)
        profit = 0

        for item_item in items:
            profit += (item_item.price - item_item.item.default_price) * item_item.amount
        return profit

    def get_expense(self, instance):
        items = InvoiceItem.objects.filter(invoice=instance)
        expense = 0

        for item_item in items:
            expense += (item_item.item.default_price) * item_item.amount
        return expense

    


class CustomerSerializer(serializers.ModelSerializer):
    customer_details = CustomerDetailSerializer()
    customer_invoices = InvoiceSerializer(many = True, read_only = True)

    class Meta:
        model = Customer
        fields = ['uuid', 'name', 'customer_details', 'customer_invoices']

    def create(self, validated_data):
        details_data = validated_data.pop('customer_details')
        customer = self.Meta.model.objects.create(shop=self.context['request'].user.employee.shop, **validated_data)

        CustomerDetail.objects.create(customer=customer, **details_data)

        return customer

    def update(self, instance, validated_data):

        details_data = validated_data.pop('customer_details')

        ser = CustomerDetailSerializer(
            instance=instance.customer_details,
            data=details_data,
            partial=True,
        )
        ser.is_valid()
        ser.save()

        instance.name = validated_data.get('name', instance.name)

        instance.save()
        return instance


class ShopDetailSerializer(serializers.ModelSerializer):


    class Meta:
        model = ShopDetail
        exclude = ['shop']

class EmployeeSerializer(serializers.ModelSerializer):


    class Meta:
        model = Employee
        exclude = ['shop']


class CategorySerializer(serializers.ModelSerializer):

    items = serializers.HyperlinkedRelatedField(read_only=True, view_name="apis:item-detail", many=True )

    class Meta:
        model = Category
        fields = ['name', 'items']

    def create(self, validated_data):
        cat = self.Meta.model.objects.create(shop=self.context['request'].user.employee.shop, **validated_data)

        return cat


class BrandSerializer(serializers.ModelSerializer):

    items = serializers.HyperlinkedRelatedField(read_only=True, view_name="apis:item-detail", many=True )

    class Meta:
        model = Brand
        fields = ['name', 'items']

    def create(self, validated_data):
        brand = self.Meta.model.objects.create(shop=self.context['request'].user.employee.shop, **validated_data)

        return brand


class ShopSerializer(serializers.ModelSerializer):
    shop_details = ShopDetailSerializer()
    shop_employees = EmployeeSerializer(many=True, read_only=True)
    shop_customers = serializers.HyperlinkedRelatedField(read_only=True, view_name="apis:customer-detail", many=True )
    #shop_cats = CategorySerializer(many=True)
    #shop_brands = CategorySerializer(many=True)
    class Meta:
        model = Shop
        fields = ('name', 'default_currency', 'shop_details', 'shop_employees','shop_customers')

    def create(self, validated_data):
        details_data = validated_data.pop('shop_details')
        shop = Shop.objects.create(**validated_data)

        ShopDetail.objects.create(shop=shop, **details_data)

        return shop

    def update(self, instance, validated_data):

        details_data = validated_data.pop('shop_details')

        ser = ShopDetailSerializer(
            instance=instance.shop_details,
            data=details_data,
            partial=True,
        )
        ser.is_valid()
        ser.save()

        instance.name = validated_data.get('name', instance.name)
        instance.default_currency = validated_data.get('default_currency', instance.default_currency)

        instance.save()
        return instance



class CurrencySerializer(serializers.ModelSerializer):


    class Meta:
        model = Currency
        fields = ['name', 'code']



class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ['user', 'shop']

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token








    