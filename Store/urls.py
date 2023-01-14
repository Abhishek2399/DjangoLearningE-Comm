from django.contrib import admin
from django.urls import path
from . import views

# changing the header of the Admin site
admin.site.site_header = "Store-Front Admin"
# changing the index of the Admin site
admin.site.index_title = "Admin"

urlpatterns = [
    path('', views.home),
    path('\my_orders', views.my_orders, name="my_orders"),
]
