from django.contrib import admin
from orders.models import ItemGroup, Item, Extras, Order, SellingArticle, CustomItem, Topping
from orders.forms import CustomItem_itemForm


class ItemAdmin(admin.ModelAdmin):
    list_display = ('itemName','size', 'price','customizable', 'itemGroup')
    list_display_links = ('itemName',)
    list_editable = ('price','customizable')

class itemsInline(admin.TabularInline):
    model = Item

class ItemGroupAdmin(admin.ModelAdmin):
    inlines = [itemsInline]

class ExtrasAdmin(admin.ModelAdmin):
    list_display = ('extra', 'price')

class ToppingAdmin(admin.ModelAdmin):
    list_display = ('toppingName', 'price')

class SellinArticlesInLine(admin.TabularInline):
    model = SellingArticle

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_date','delivered', 'total_price')
    inlines = [ SellinArticlesInLine, ]
    list_editable = ('delivered',)

class SellingAdmin(admin.ModelAdmin):
    pass


class CustomItemAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'total_price')
    form = CustomItem_itemForm
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)




admin.site.register(ItemGroup, ItemGroupAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Extras, ExtrasAdmin)
admin.site.register(Topping, ToppingAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(SellingArticle, SellingAdmin)
admin.site.register(CustomItem,CustomItemAdmin)

