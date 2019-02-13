from django.db import models
from django.conf import settings


class ItemGroup(models.Model):
    itemGroup = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return "Id: " + str(self.id)+ " "+ str(self.itemGroup)

class Item(models.Model):
    itemName = models.CharField(max_length=30)
    itemGroup = models.ForeignKey('ItemGroup', on_delete=models.CASCADE)
    price = models.FloatField()

    SIZE_CHOICES = (
        ('', ''),
        ('sm', 'Small'),
        ('lg', 'Large')
    )
    size = models.CharField(
        max_length=20, 
        blank=True,
        choices=SIZE_CHOICES,
        default=''
        )


    class Meta:
        unique_together = (('itemName', 'size', 'itemGroup'),)
        #ordering = ('itemGroup__itemGroup',)
    
    def __str__(self):
        return str(self.itemName) +" "+ str(self.size) + " ItemG: " + str(self.itemGroup)

class CustomItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    item = models.OneToOneField(Item, on_delete=models.CASCADE,primary_key=True)
    extra = models.ManyToManyField('Extras')
    topping = models.ManyToManyField('Topping')

    def _get_itemName(self):
        toppings = self.topping.all()
        extras = self.extra.all()

        if len(extras) > 0:
            s = ""
            for e in extras:
                s = s+ " +" + e.extra
            return self.item.itemName + s
        elif len(toppings) > 0:
            s = ""
            for t in toppings:
                s = s+ " +" + t.toppingName
            return self.item.itemName + s
        return self.item.itemName

    full_name = property(_get_itemName)

    def _get_price(self):
        toppings = self.topping.all()
        extras = self.extra.all()

        if len(extras) > 0:
            p = 0.0
            for i in extras:
                p = p + i.price
            return self.item.price + p
        elif len(toppings) > 0:
            p = 0.0
            for i in toppings:
                p = p + i.price
            return self.item.price + p
        return self.item.price
    
    total_price = property(_get_price)



class Extras(models.Model):
    extra = models.CharField(max_length=30)
    price = models.FloatField()

    def __str__(self):
        return "ID: " + str(self.extra) + " " + str(self.extra)

class Topping(models.Model):
    toppingName = models.CharField(max_length=30)
    price = models.FloatField(default=0.0)
    def __str__(self):
        return "ID: " + str(self.id) + " " + str(self.toppingName)

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  "ID: " + str(self.id)

class SellingArticle(models.Model):
    sell_order = models.ForeignKey('Order', on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

