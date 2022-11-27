from django.shortcuts import render, HttpResponse
from django.db.models import Q, F
# for aggregation function
from django.db.models.aggregates import *
# for annotation
from django.db.models import Value, F, Func
# for DB Functions
from django.db.models.functions import Concat
from pprint import pprint
from .models import *
import pandas as pd


# Create your views here.
def home(request):
    result = {}
    cust = Customer.objects.all()[5]
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
    columns = [str(col).title() for col in objects.columns.to_list()]
    objects = objects.to_dict('records')
    pprint(columns)

    

    cdict = {
        'columns' : columns,
        'object_list' : objects,
        'result' : result,
        'key' : list(result.keys())[0] if result else None,
        'result_head' : "Aggregate function Count"
    }
    return render(request, "home.html", context=cdict)

    # annotating a new col "is_new" and giving it a True value, and new_id taking values from pre-existing cols
    objects = pd.DataFrame(Product.objects.annotate(is_new = Value(True), new_id= F('id')+F('unit_price')).values())

    # counting the number of Products using the aggregate function, it will not return a queryset but a dictionary 
    result = Product.objects.aggregate(product_count = Count('id'), min_price = Min('unit_price'))
    
    objects = Product.objects.prefetch_related('promotions').all()# this will get the fields from Product table as well as the Collection table, select_related will only work on one to many fields
    # print(products[0].promotions.all())

    # querying the related fields as well 
    objects = Product.objects.all() # this will only get fields from the Product table
    
    # in-order to the get the field from the related tables at the same time
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
