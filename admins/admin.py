from django.contrib import admin
from .models import*
from Users.models import*
# Register your models here.

#  Admin Table



#-----------------------------------------

class Company_view(admin.ModelAdmin):
    list_display=('id','name','image','status')
admin.site.register(Companys,Company_view)

#-----------------------------------------

class Product_view(admin.ModelAdmin):
    list_display=('id','name','category','company','price','des','image','status')
admin.site.register(Products,Product_view)

#--------------------------------------------

class Customer_view(admin.ModelAdmin):
    list_display=('id','fname','lname','email','phone','pass1','image','dob','status')
    
admin.site.register(Customer,Customer_view)

#----------------------------------------------

class Shoping_view(admin.ModelAdmin):
    list_display=('p_id','p_name','p_quantity','p_price','p_image','p_date','cust_address','status')
admin.site.register(Shoping,Shoping_view)

#-------------------------------------------------

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    # Columns shown in admin list view
    list_display = (
        'id',
        'cid',
        'fullname',
        'phone',
        'city',
        'state',
        'country',
        'pincode',
        'status',
    )

    # Filters on right sidebar
    list_filter = ('state', 'country', 'status')

    # Search box fields
    search_fields = (
        'fullname',
        'phone',
        'alt_phone',
        'city',
        'state',
        'country',
        'pincode',
        'cid__email',   # search by customer email
    )

    # Pagination
    list_per_page = 25

    # Editable fields directly from list view
    list_editable = ('status',)

    # Default ordering
    ordering = ('-id',)

    # Field grouping in detail page
    fieldsets = (
        ('Customer Info', {
            'fields': ('cid', 'fullname', 'phone', 'alt_phone')
        }),
        ('Address Details', {
            'fields': ('house', 'area', 'city', 'state', 'country', 'pincode')
        }),
        ('Status', {
            'fields': ('status',)
        }),
    )