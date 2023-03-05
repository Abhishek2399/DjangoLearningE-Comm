# serializer that we will be using for conversion
from rest_framework import serializers
from decimal import Decimal
from .models import Product, Collection


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'no_of_product', 'collection_update']
    
    no_of_product = serializers.SerializerMethodField(method_name = "get_no_of_products")
    collection_update = serializers.HyperlinkedRelatedField(
        queryset = Collection.objects.all(),
        view_name = "collection-detail",
        source = "id",
        required = False
    )

    def get_no_of_products(self, collection : Collection):
        return collection.product_set.count() #type:ignore

        

# class CollectionSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length = 255)


# # the class being mentioned here is the serializer we will be using convert python-django oebjects to dictionary
# class ProductSerializer(serializers.Serializer):
#     # here we need to include all the fields we want to serialize from the Product model
#     # never to mention confidential fields of the objects
#     # there will always be 2 representation of the object one is internal which refers to the model class and another one refers to the one being accessed from the endpoint(JSON)
#     id = serializers.IntegerField()
#     # this is similar to defining models in the model class
#     title = serializers.CharField(max_length=255)
#     # unit_price = serializers.DecimalField(max_digits=6, decimal_places=2) # renaming the above field for which we have to let the field know the source of the field
#     price = serializers.DecimalField(max_digits=6, decimal_places=2, source = "unit_price")
#     # creating a custom field which can be a method extracting and processing the data we want
#     price_with_tax = serializers.SerializerMethodField(method_name = "calculate_tax")

#     # serializing the relationship, as collection is a foreign key in our table
#     # following will return the object id
#     collection_field = serializers.PrimaryKeyRelatedField(
#         queryset = Collection.objects.all(),
#         source = "collection"
#     )
    
#     # we can also access the related field in terms of string as follows, will execute large number of queries as it will iterate through all the collection object and bring the title
#     collection_str_rep = serializers.StringRelatedField(source = "collection")

#     # to resolve the issue of large queries, just create the serializer of foreign-object and use it directly
#     collection_obj = CollectionSerializer(source="collection")

#     # instead of giving the object we can provide an Hyperlink to the end-point for viewing the selection
#     collection_hyperL = serializers.HyperlinkedRelatedField(
#         queryset = Collection.objects.all(),
#         view_name = "collection-detail", # name given to the url path in the urls.py
#         source = "collection"
#     )

#     product_hyperL = serializers.HyperlinkedRelatedField(
#         queryset = Product.objects.all(),
#         view_name = "product-detail", # name given to the url path in the urls.py
#         source = "id"
#     )

#     # the method that will be called by the custom field
#     def calculate_tax(self, product : Product):
#         return product.unit_price * Decimal(1.1)
    

# defining the above class using a short-hand method aka "ModelSerializer" ==> similar to the model forms
# uses model directly to create attr.
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price', 'description', 'slug', 'inventory', 'price_with_tax', 'collection', 'product_update'] # we can define the fields we want to serialize explicitly here as a list
        # fields = '__all__' # this will consider all the fields from the model specified which is not a proper practice, always explicitly define the fields we want to have
        read_only_fields = ['product_update']
    
    # for fields that we want to display as extra we can define outside the Meta class, which will over-write the default value
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset = Collection.objects.all(),
    #     view_name = "collection-detail"
    # )

        # collection_obj = CollectionSerializer(source = "collection")

    price_with_tax = serializers.SerializerMethodField(method_name = "calculate_tax")
    product_update = serializers.HyperlinkedRelatedField(
        queryset = Product.objects.all(),
        view_name = "product-detail",
        source = "id",
        required = False
    )
    # we can define the custom fields as well outside the Meta class
    def calculate_tax(self, product : Product):
        return product.unit_price * Decimal(1.1)

    # defining custom validations, just an example for custom validation not actually being used in the model
    # def validate(self, data:dict) -> object:
    #     if data['password'] != data['new password']:
    #         return serializers.ValidationError("Password does not match")
    #     return data
    
    # overwriting the method responsible for saving the object in the database
    # following create method is already called whenever the save method is called
    # def create(self, validated_data:dict={}) -> Product:
    #     print("Inserting an object")
    #     product = Product(**validated_data)
    #     # product.other = 1 # here we can access any attribute belonging the Product class
    #     product.save()
    #     return product
    
    # Overwritting the update function 
    # instance is set by django itself
    # def update(self, instance:Product, validated_data:dict={}) -> Product:
    #     print("Updating an object")
    #     # defining the field we want to update can be anything
    #     instance.unit_price = validated_data.get('unit_price', Decimal(0))
    #     instance.save()
    #     return instance

