# serializer that we will be using for conversion
from rest_framework import serializers
from decimal import Decimal
from .models import Product

# the class being mentioned here is the serializer we will be using convert python-django objects to dictionary
class ProductSerializer(serializers.Serializer):
    # here we need to include all the fields we want to serialize from the Product model
    # never to mention confidential fields of the objects
    # there will always be 2 representation of the object one is internal which refers to the model class and another one refers to the one being accessed from the endpoint(JSON)
    id = serializers.IntegerField()
    # this is similar to defining models in the model class
    title = serializers.CharField(max_length=255)
    # unit_price = serializers.DecimalField(max_digits=6, decimal_places=2) # renaming the above field for which we have to let the field know the source of the field
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source = "unit_price")
    # creating a custom field which can be a method extracting and processing the data we want
    price_with_tax = serializers.SerializerMethodField(method_name = "calculate_tax")
    # the method that will be called by the custom field
    def calculate_tax(self, product : Product):
        return product.unit_price * Decimal(1.1)