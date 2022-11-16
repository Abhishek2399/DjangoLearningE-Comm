from enum import auto
from random import choices
from statistics import mode
from unicodedata import decimal
from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.


# Many to many 
# we can promote multiple products
# one product can appear in multiple promotions
class Promotion(models.Model):
    description = models.CharField(max_length = 255)
    discount = models.FloatField(max_length = 255)


class Collection(models.Model):
    title = models.CharField(max_length=255)
    # to resolve the circular relationship in between the Collection and Product class we have to add the Foreign class in quotes '' make sure the name remains the same as the actual class
    # after resolving the circular relation we will have to change the related name as well to '+'


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2) # preferred more then FloatField because Float has rounding issues
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True) # auto_add_now will add the date and time when the field is updated/added first time
    # django will use the related_name field in the Promotion class as reference to the product class from Promotion class
    # promotions = models.ManyToManyField(Promotion, related_name="products")
    promotions = models.ManyToManyField(Promotion)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)


class Customer(models.Model):
    # setting the deafult Value
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    # setting up the choices
    MEMBERSHIP_CHOICES = [
        # ('value_stored_db', 'human_readable_name')
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    # following is a choice field
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default = MEMBERSHIP_BRONZE)


class Order(models.Model):
    PAYMENT_PENDING = 'P'
    PAYMENT_COMPLETE = 'C'
    PAYMENT_FAILED = 'F'

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_PENDING, 'Pending'),
        (PAYMENT_COMPLETE, 'Complete'),
        (PAYMENT_FAILED, 'Failed'),
    ]
    # django will automatically populate this field
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_PENDING)


class Address(models.Model):
    street = models.CharField(max_length = 255)
    city = models.CharField(max_length = 255)
    # when we delete the customer the address will be deleted 
    # one address will be related to one customer
    # cutomer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    # incase we need one to many relation i.e. one customer can have multiple addresses
    cutomer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    # here the models.PROTECT will protect from deletion of the Products even if any customer is Deleted
    collection = models.ForeignKey('Collection', on_delete=models.PROTECT)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Cart(models.Model):
    # following field will be populated when the object of following class is created, only when it is created
    # is we want this field to be updated when the object is edited we need to use the "auto_now" attribute instead of "auto_now_add"
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

