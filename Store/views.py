
from django.shortcuts import render, HttpResponse
from django.db.models import Q, F
# for aggregation function
from django.db.models.aggregates import *
# for annotation
from django.db.models import Value, F, Func, ExpressionWrapper, DecimalField
# for DB Functions
from django.db.models.functions import Concat
from django.db import transaction, connection
from pprint import pprint
from .models import Product, Order, Customer, Collection
import pandas as pd

# generic models
from django.contrib.contenttypes.models import ContentType
from Tags.models import TaggedItem, Tag


# Create your views here.
def home(request):
    print("view called")
    import random
    result = {}
    ids = [order['id'] for order in Order.objects.all().values('id')]
    random_id = random.choice(ids)
    print(f"ID : {random_id}")
    model = Product
    objects = pd.DataFrame(
        model.objects.all().values()
    )
    columns = [str(col).title() for col in objects.columns.to_list()]
    objects = objects.to_dict('records')

    cdict = {
        'columns' : columns,
        'object_list' : objects,
        'result' : result,
        'key' : list(result.keys())[0] if result else None,
        'result_head' : "Aggregate function Count"
    }
    return render(request, "home.html", context=cdict)

    
    # executing SQL queries independent from any Model
    # 1. Establish connection with the DB
    cursor = connection.cursor()
    # 2. pass the query we want to execute
    cursor.execute('')
    # 3. close connection
    cursor.close()

    # alternate and safe way to write the above process
    with connection.cursor() as cursor:
        cursor.execute('')
        # executing store procedures
        cursor.callproc('proc_name',['params'])


    # executing raw SQL Queries, every manager has a raw method
    orders = Order.objects.raw('Select * from Order')

    # transaction is used when we want to perfrom multiple insertions together and if one of them fails none other should take place
    with transaction.atomic():
        # write the queries here whcih we want to be atomic
        # usecase : if there is no order item there should be no order
        order = Order()
        order.customer = Customer.objects.all().first()
        order.save()

        order_item = OrderItem()
        order_item.order = order
        order_item.product_id = -1 # giving wrong id to generate an error
        order_item.quantity = 2
        order_item.unit_price = 10
        order_item.save()


    
    # creating objects
    # creating the object we want to fill
    collection = Collection()
    # fill in the attribute values, these will reflect in the cols of respective table
    collection.title = "Video Games"
    collection.featured_product = Product.objects.get(pk = 500)  # type: ignore
    # saving the object/entry
    collection.save()

    # custom manager class, code available in the model of repective app i.e. Tags.models
    item_tags = TaggedItem.objects.get_tags_for(object_type=Product, object_id=10)

    # Generic Object Relationship 
    # special method 
    content_type = ContentType.objects.get_for_model(model=Product)
    tag_items = TaggedItem.objects.select_related('tag').filter(
            content_type = content_type,
            object_id = 10
    )


    # creating complex expressions
    # first create the expression wrapper object and later use it in query, just to keep the code clean
    # calculating a discounted price and annotating it 
    discounted_price = ExpressionWrapper(F('unit_price') * 0.8, output_field=DecimalField())
    objects = pd.DataFrame(
        Product.objects.annotate(discounted_price = discounted_price).values()
    )

    # following query will get us the count of orders grouped by the Customer-id, i.e. no. of orders for each customer 
    objects = pd.DataFrame(
        Customer.objects.annotate(order_count = Count('my_orders')).values()
        )

    # using the database level functions.
    # syntax : create one new col using annotate =>'full_name'.
    # use the cols from table itself if needed using the 'F' object, => F('first_name'), F('last_name').
    # wrap the fields referenced using F-objs in a Func class, this will be needed to let the DB know we are sending the params wrapped in the Func class as args, => Func(F('first_name'), F('last_name')).
    # pass the function name we want to use from the database to the same Func class.
    objects = pd.DataFrame(
        Customer.objects.annotate(
                full_name = Concat(F('first_name'), Value(' '), F('last_name'))
            ).values()
        )

    # annotating a new col "is_new" and giving it a True value, and new_id taking values from pre-existing cols
    objects = pd.DataFrame(Product.objects.annotate(is_new = Value(True), new_id= F('id')+F('unit_price')).values())

    # counting the number of Products using the aggregate function, it will not return a queryset but a dictionary 
    result = Product.objects.aggregate(product_count = Count('id'), min_price = Min('unit_price'))
    
    objects = Product.objects.prefetch_related('promotions').all()# this will get the fields from Product table as well as the Collection table, select_related will only work on one to many fields
    # print(products[0].promotions.all())

    # querying the related fields as well 
    objects = Product.objects.all() # this will only get fields from the Product table
    
    # in-order to the get the field from the related tables at the same time ,
    # reduces the number of queries required while fetching the foreign objects, if select-related not used foreign objects can be accessed but will require too many queries
    objects = Product.objects.select_related('collection').all() # this will get the fields from Product table as well as the Collection table, select_related will only work on one to many fields. 
    
    objects = Product.objects.select_related('collection__featured_product').all() # we can also get the fields related to the related field in query i.e. related fields to the collection object

    # checking if the object exist
    promotion_exist = Promotion.objects.filter(pk=1).exists()
    
    # finding all the products with price greater than 1000
    objects = Product.objects.filter(price__gt =  1000)
    
    # finding products in range of price
    objects = Product.objects.filter(price__range = (100, 500))

    # evaluating and executing Query set
    # products = list(products)
    
    # using 'F' queries to compare two attributes of same or different models
    # sorting the products we can do it by the order_by method and passing it the fields we want to sort on, default is the ascending order by using '-' symbol along with the field name will sort in descending order
    # if we are using 2 attributes first the result will be sorted based on first attribute and then the result will be sorted on the 2nd attribute
    objects = Product.objects.filter(price__gt = F('inventory')).order_by('inventory', '-title')

    # limiting the results
    objects = Product.objects.all()[:5]
    objects = Product.objects.all()[5:10]

    # selecting only specific fields, only title and price values will be selected and displayed
    # following query will return a list of dictionary instead of query sets
    objects = Product.objects.all().values('title', 'price')



# for testing the use of related name field
def my_orders(request):
    customer = Customer.objects.all()[5]
    print(f"Customer : {customer}")
    # getting the products ordered by following customer
    objects = pd.DataFrame(customer.my_orders.all()[0].my_order_items.all().values())  # type: ignore

    columns = [str(col).title() for col in objects.columns.to_list()]
    objects = objects.to_dict('records')
    pprint(columns)
    cdict = {
        "object_list" : objects,
        "columns" : columns
    }
    return render(request, "my_products.html", context=cdict)
    return HttpResponse(objects)


# all the functions/views mentioned below are the REST-APIs
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
# to use the resp/req from the rest-framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer, CollectionSerializer
from rest_framework import status # used for responding multiple status
# using Django HTTP-Response
# def product_list(reponse):
    # return HttpResponse('ok')

# converting the above code as per the REST
# in the list we have defined the HTTP-Methods that our end-point will manage hence in the following end point we can either review all the objects (GET) or create a new one (POST)
@api_view(['GET', 'POST'])
def product_list(request):

    if request.method == "GET":
        product_qs = Product.objects.all()
        products_serialzs = ProductSerializer(product_qs, many = True, context = {'request' : request}) # many attr. will let the serializer know that it has to iterate through the queryset
        return Response(products_serialzs.data)
    elif request.method == "POST":
        product_dserializ = ProductSerializer(data = request.data) # this is where the de-serializing takes place
        
        # extracting the data from the de-serialized object
        # if product_dserializ.is_valid(): # check if the de-serialized object is valid
        #     data = product_dserializ.validated_data # extract the data if valid
        #     return Response('ok')
        # else:
        #     # if form not valid send a bad request status along with the errors 
        #     return Response(product_dserializ.errors, status = status.HTTP_400_BAD_REQUEST)

        # short hand for the above
        product_dserializ.is_valid(raise_exception=True) # following will raise exception and return a 400 request along with errors at the same time
        try:
            product_dserializ.save() # save method will itself extract the data by using .validated_data internally
        except Exception as e:
            return Response(status=status.HTTP_409_CONFLICT) # returning a conflict status in case of any constraint error
        print(product_dserializ.validated_data)
        return Response(product_dserializ.data, status=status.HTTP_201_CREATED) # if new object successfully created return the response 201 : i.e. object created 
    

# will send a single product object
# following end-point will handle 2 types of request get and put, get will help us fetch the object and put method will help us update the object,
# rule endpoint that will handle the put-request should access only single object
@api_view(['GET', 'PUT', 'DELETE']) 
def product_detail(request, pk):
    # try:
    #     product_obj = Product.objects.get(pk = id)
    #     product_serialz = ProductSerializer(product_obj)
    # except Product.DoesNotExist:
    #     # return Response(status = 404) # avoid sending numbers in response as it can be confusing
    #     return Response(status = status.HTTP_404_NOT_FOUND)

    # we can wrap the whole logic using a shortcut method 'get_object_or_404'
    product_obj = get_object_or_404(Product, pk = pk)
    if request.method == "GET":
        product_serialz = ProductSerializer(
            product_obj, # product object
            context={'request' : request} # for showing the link to go to any object
        )
        return Response(product_serialz.data)
    elif request.method == "PUT":
        # initializing with the current Product
        product_dserialz = ProductSerializer(
            product_obj, # product object
            data = request.data, # edited data from the request
            context={'request' : request} # for showing the link in the object
        )
        product_dserialz.is_valid(raise_exception=True)
        product_dserialz.save()
        return Response(product_dserialz.data, status = status.HTTP_201_CREATED)
    elif request.method == "DELETE":
        # whenever we delete a product return an empty respone of 204-no Content
        # before deleting product check if it has been used as any foreign key
        if product_obj.my_ordered_products.count() > 0:
            return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)
        product_obj.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
    
@api_view(['get', 'put', 'delete'])
def collection_detail(request, pk):
    collection_obj = get_object_or_404(Collection, pk = pk)
    collection_serialz = CollectionSerializer(collection_obj, context = {'request':request})
    
    return Response(collection_serialz.data)


@api_view(['GET', 'POST'])
def collection_list(request):
    collection_qs = Collection.objects.all()
    if request.method == "GET":
        collection_serialzs = CollectionSerializer(collection_qs, many = True, context = {'request':request})
        return Response(collection_serialzs.data)
    elif request.method == "POST":
        collection_serialz = CollectionSerializer(data=request.data, context = {'request':request})
        collection_serialz.is_valid(raise_exception=True)
        try:
            collection_serialz.save()
        except Exception as e:
            return Response(status = status.HTTP_409_CONFLICT)
        return Response(collection_serialz.data, status = status.HTTP_201_CREATED)
