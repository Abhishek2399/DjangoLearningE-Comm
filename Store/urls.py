from django.contrib import admin
from django.urls import path
from . import views

# changing the header of the Admin site
admin.site.site_header = "Store-Front Admin"
# changing the index of the Admin site
admin.site.index_title = "Admin"

urlpatterns = [
    path('', views.home),
    path('my_orders', views.my_orders, name="my_orders"),
    # all the paths below this refer to the APIs endpoint
    path('products/', views.product_list, name="all-products"), # if someone access the 'products/' end pioint it will be handeled by the productlist from the views
    path('products/<int:pk>', views.product_detail, name="product-detail"),
    path('collections/<int:pk>', views.collection_detail, name="collection-detail"),
    path('collections/', views.collection_list, name="all-collections"),

]
