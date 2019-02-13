from django.contrib import admin
from .models import ItemGroup, Item, Extras, Order, SellingArticle, CustomItem, Topping


class ItemAdmin(admin.ModelAdmin):
    list_display = ('itemName','size', 'price', 'itemGroup')
    list_display_links = ('itemName',)
    list_editable = ('price',)


class ExtrasAdmin(admin.ModelAdmin):
    list_display = ('extra', 'price')

class ToppingAdmin(admin.ModelAdmin):
    list_display = ('toppingName', 'price')
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_date')

class SellingAdmin(admin.ModelAdmin):
    pass

class CustomItemAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'total_price')



admin.site.register(ItemGroup)
admin.site.register(Item, ItemAdmin)
admin.site.register(Extras, ExtrasAdmin)
admin.site.register(Topping, ToppingAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(SellingArticle, SellingAdmin)
admin.site.register(CustomItem,CustomItemAdmin)