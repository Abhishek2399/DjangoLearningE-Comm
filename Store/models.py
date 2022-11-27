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

    def __str__(self) -> str:
        return f"{self.description} : {self.discount}"


class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product', related_name="+", on_delete=models.SET_NULL, null=True)
    # to resolve the circular relationship in between the Collection and Product class we have to add the Foreign class in quotes '' make sure the name remains the same as the actual class
    # after resolving the circular relation we will have to change the related name as well to '+'
    def __str__(self):
        return f"{self.title}"

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

    class Meta:
        # defining meta data about the current class, we use the following class in order to customize the following table
        db_table = "store_customer"
        indexes = [
            models.Index(fields=['first_name', 'last_name'])
        ]

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} ({self.membership})"

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
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, null=True, related_name="my_orders")

    def __str__(self) -> str:
        return f"{self.placed_at} - {self.customer} - {self.payment_status}"


class Address(models.Model):
    street = models.CharField(max_length = 255)
    city = models.CharField(max_length = 255)
    # when we delete the customer the address will be deleted 
    # one address will be related to one customer
    # cutomer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    # incase we need one to many relation i.e. one customer can have multiple addresses
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.street}, {self.city}"


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(null=True, default="-")
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    # here the models.PROTECT will protect from deletion of the Products even if any customer is Deleted
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion, related_name="promoted_product")


    def __str__(self):
        return f"{self.collection} : {self.title} - {self.description}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="my_order_items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="my_ordered_products")
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.order} - {self.product} - {self.quantity} - {self.unit_price}"


class Cart(models.Model):
    # following field will be populated when the object of following class is created, only when it is created
    # is we want this field to be updated when the object is edited we need to use the "auto_now" attribute instead of "auto_now_add"
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

