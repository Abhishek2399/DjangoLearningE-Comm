from django.contrib import admin, messages
from django.http import HttpRequest
from .models import *
from Tags.models import TaggedItem, Tag
from django.db.models.aggregates import Count
# html links 
from django.utils.html import format_html, urlencode
from django.urls import reverse
from django.db.models.query import QuerySet

# generic relations
from django.contrib.contenttypes.admin import GenericTabularInline

# customizing the list page, where all the objects are displayed from the table
# method-1
# we can name the class anything but preferred naming conventino is <Modelname>Admin
# class CollectionAdmin(admin.ModelAdmin):
#     # if we want to display specific fields
#     list_display = ['title', 'featured_product']


# creating custom-filters 
class InventoryFilter(admin.SimpleListFilter):
    title = "inventory"
    parameter_name = "inventory"
    # we need to overwrite 2-methods here 
    # this method is used to display the filter we want on the page
    def lookups(self, request, model_admin) :
        return [('<10', 'Low'), ('>10', 'High')] # first value in the tuple is the human readable equivalent of the filter
    
    def queryset(self, request, queryset: QuerySet):
        filter_val = self.value()
        print(f"filter_val : {self.value()}")
        if filter_val == "<10":
            return queryset.filter(inventory__lt = 10)
        if filter_val == ">10":
            return queryset.filter(inventory__gt = 10)


class TagInline(GenericTabularInline):
    model = TaggedItem
    extra = 0
    min_num = 0


# method-2
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # custom forms on the admin page
    autocomplete_fields = ['collection'] # for this we need to add the searchfield in the Admin setting of the collection we are using
    # field = [] # here we can specify the fields we want to show to the user
    # readonly_fields = [] # fields specified here cannot be changed from the admin panel
    prepopulated_fields = {"description": ("title",)}    
    # custom actions
    actions = ['clear_inventory']
    list_display = ['id', 'title', 'description', 'unit_price', 'inventory', 'inventory_status', 'collection_title']
    # fields that we want to be editable, using the following we wont need to open any of the object in order to edit it in the admin panel
    list_editable = ['title', 'description', 'unit_price']
    # ordering the objects wrt to specific field
    ordering = ['inventory'] # ascending order
    # ordering = ['-inventory'] # descending order
    # number of items we want to display per page
    list_per_page = 10
    # preloading the related-obejcts
    list_select_related = ['collection']
    # adding filteration to the data
    list_filter = ['collection', 'last_update', InventoryFilter] # class added is the custom filter

    search_fields = ['title']

    inlines = [TagInline] # for getting the child

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


    # custom actions on the admin-page 
    @admin.action(description="Clear Inventory")
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory = 0)
        # sending the status message to the user
        self.message_user(
            request, 
            f"{updated_count} Successfully Updated",
        )


class OrderItemInline(admin.TabularInline): # tabular inline to display chlidren in tabular format, we can use StackedInline to stack the children
    autocomplete_fields = ['product']
    model = OrderItem
    extra = 0
    min_num = 0
    max_num = 10


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    actions = ['payment_complete']
    list_display = ['placed_at', 'payment_status', 'customer_name']
    list_select_related = ['customer']
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]

    def customer_name(self, order):
        return f"{order.customer.first_name} {order.customer.last_name}"

    @admin.action(description = "Payment Compelted")
    def payment_complete(self, request, queryset):
        updated_count = queryset.update(payment_status = Order.PAYMENT_COMPLETE)
        self.message_user(
            request, 
            f"{updated_count} Successfully Updated",
        )



@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    # here we dont actually have the field product_count in the collection model
    # we will have to annotate this field in the queryset
    list_display = ['id', 'title', 'product_count']
    search_fields = ['title']


    @admin.display(ordering='product_count')
    def product_count(self, collection):
        # return collection.product_count
        # converting the above vlaue to a link, we can do that by formatting the value in link 
        # param1 - url where we want to redirect, param2 - the link text
        # return format_html("<a href='\store'>{}</a>", collection.product_count)
        # if we want to redirect to another admin page
        # as the url might change in the future we can ask django for the url
        # syntax for getting the url "admin:appname_model_page", the page that we see after clicking on any model in the admin is the "change_list"
        # we can also add query-string which is url consisting of query
        url = (
            reverse("admin:Store_product_changelist")
            + '?'
            + urlencode({ # used to pass the parameter, we can add multiple params in the dictionary
                'collection__id' : str(collection.id)
            }))
        return format_html("<a href='{}'>{}</a>", url, collection.product_count)

    # following method will return a modified queryset as per our need
    def get_queryset(self, request: HttpRequest):
        return super().get_queryset(request).annotate(
            product_count = Count('product')
        )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'birth_date', 'email', 'phone', 'membership', 'my_order_count']
    list_per_page = 10
    list_editable = ['membership']
    # for searching in the admin page
    # search_fields = ['first_name', 'last_name'] # this will search all the chars in the first name and last name
    # search_fields = ['first_name__startswith', 'last_name__startswith'] # this will search only the customer who's firstname and lastname start with a specific char.
    search_fields = ['first_name__istartswith', 'last_name__istartswith'] # similar as above but case-insensitive
    


    def name(self, customer):
        return f"{customer.first_name} {customer.last_name}"

    @admin.display(ordering="first_name") # check why not working later
    def my_order_count(self, customer):
        # return len(list(customer.my_orders.all().values()))
        url = (
            reverse("admin:Store_order_changelist")
            + '?'
            + urlencode({
                'customer__id' : customer.id
            })
            )
        return format_html("<a href = '{}'>{}</a>", url, customer.order_count)

        
    def get_queryset(self, request: HttpRequest):
        return super().get_queryset(request).annotate(
            order_count = Count('my_orders')
        )

# @admin.register(Tag)
# class TagAdmin(admin.ModelAdmin):
#     search_fields = ['label']



# Register your models here.
admin.site.register(Promotion)
# register the model along with the Admin settings
# admin.site.register(Collection)
# admin.site.register(Customer)
admin.site.register(Address)
# admin.site.register(Product)
# admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(CartItem)
# admin.site.register(Tag)
admin.site.register(TaggedItem)

