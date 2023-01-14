from django.contrib import admin
from django.http import HttpRequest
from .models import *
from Tags.models import TaggedItem, Tag
from django.db.models.aggregates import Count


# customizing the list page, where all the objects are displayed from the table
# method-1
# we can name the class anything but preferred naming conventino is <Modelname>Admin
# class CollectionAdmin(admin.ModelAdmin):
#     # if we want to display specific fields
#     list_display = ['title', 'featured_product']


# method-2
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'unit_price', 'inventory_status', 'collection_title']
    # fields that we want to be editable, using the following we wont need to open any of the object in order to edit it in the admin panel
    list_editable = ['title', 'description', 'unit_price']
    # ordering the objects wrt to specific field
    ordering = ['inventory'] # ascending order
    # ordering = ['-inventory'] # descending order
    # number of items we want to display per page
    list_per_page = 10
    # preloading the related-obejcts
    list_select_related = ['collection']

    # computed columns
    # sorting the computed field
    # @admin.display(ordering="inventory")
    def inventory_status(self, product):
        if product.inventory < 10 : return "Low"
        else: return "Ok"

    # method to get specific field from the related objects
    def collection_title(self, product):
        return product.collection.title

    # showing related fields
    list_display += ['collection']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['placed_at', 'payment_status', 'customer_name']
    list_select_related = ['customer']

    def customer_name(self, order):
        return f"{order.customer.first_name} {order.customer.last_name}"


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    # here we dont actually have the field product_count in the collection model
    # we will have to annotate this field in the queryset
    list_display = ['title', 'product_count']

    @admin.display(ordering='product_count')
    def product_count(self, collection):
        return collection.product_count

    # following method will return a modified queryset as per our need
    def get_queryset(self, request: HttpRequest):
        return super().get_queryset(request).annotate(
            product_count = Count('product')
        )


# Register your models here.
admin.site.register(Promotion)
# register the model along with the Admin settings
# admin.site.register(Collection)
admin.site.register(Customer)
admin.site.register(Address)
# admin.site.register(Product)
# admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Tag)
admin.site.register(TaggedItem)

