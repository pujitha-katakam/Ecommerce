# admin.py
'''
from django.contrib import admin
from .models import Catg, SubCatg,prodss,prod_type

class SubCategoryInline(admin.TabularInline):
    model = SubCatg


class CategoryAdmin(admin.ModelAdmin):
    inlines = [SubCategoryInline]


admin.site.register(Catg, CategoryAdmin)
admin.site.register(SubCatg)
admin.site.register(prodss)
admin.site.register(prod_type)'''

from django.contrib import admin
from .models import Catg, SubCatg, prodss, prod_type,Customer,Cart,Orders,Buynow

class SubCategoryInline(admin.TabularInline):
    model = SubCatg

class ProductTypeInline(admin.TabularInline):
    model = prod_type.categories.through

class CategoryAdmin(admin.ModelAdmin):
    inlines = [SubCategoryInline]

class SubCategoryAdmin(admin.ModelAdmin):
    inlines = [ProductTypeInline]

@admin. register(Customer)
class CustomerModelAdmin(admin.ModelAdmin) :
    list_display = ['id', 'user', 'locality', 'city', 'state', 'zipcode']

 
admin.site.register(Catg, CategoryAdmin)
admin.site.register(SubCatg, SubCategoryAdmin)
admin.site.register(prodss)
admin.site.register(prod_type)
admin.site.register(Cart)
admin.site.register(Orders)
admin.site.register(Buynow)

