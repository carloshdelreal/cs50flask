from django.contrib import admin
from .models import ItemGroup, Item, Extras, MenuItem


class ItemAdmin(admin.ModelAdmin):
    list_display = ('itemName', 'price', 'itemGroup')

class ExtrasAdmin(admin.ModelAdmin):
    list_display = ('extra', 'price', 'itemGroup')

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('itemGroup', 'item', 'price')
    
admin.site.register(ItemGroup)
admin.site.register(Item, ItemAdmin)
admin.site.register(Extras, ExtrasAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
