from django.shortcuts import render, HttpResponse
from django.db.models import Q, F
from pprint import pprint
from .models import *

# Create your views here.
def home(request):
    # checking if the object exist
    promotion_exist = Promotion.objects.filter(pk=1).exists()
    # finding all the products with price greater than 1000
    products = Product.objects.filter(price__gt =  1000)
    # finding products in range of price
    products = Product.objects.filter(price__range = (100, 500))
    
    # evaluating and executing Query set
    # products = list(products)
    
    # using 'F' queries to compare two attributes of same or different models
    # sorting the products we can do it by the order_by method and passing it the fields we want to sort on, default is the ascending order by using '-' symbol along with the field name will sort in descending order
    # if we are using 2 attributes first the result will be sorted based on first attribute and then the result will be sorted on the 2nd attribute
    products = Product.objects.filter(price__gt = F('inventory')).order_by('inventory', '-title')

    # limiting the results
    products = Product.objects.all()[:5]
    products = Product.objects.all()[5:10]

    # selecting only specific fields, only title and price values will be selected and displayed
    # following query will return a list of dictionary instead of query sets
    products = Product.objects.all().values('title', 'price')


    return render(request, "home.html", context={'products' : products})


def my_orders(request):
    customer = Customer.objects.all().first()
    # getting the products ordered by following customer
    order_items = Customer.objects.all().first().my_orders.all().first().my_order_items.all()
    cdict = {
        "ordered_items" : order_items
    }
    return render(request, "my_products.html", context=cdict)
