from django.db import models


class ItemGroup(models.Model):
    itemGroup = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.itemGroup

class Item(models.Model):
    itemName = models.CharField(max_length=30)
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
    price = models.FloatField()
    itemGroup = models.ForeignKey('ItemGroup', on_delete=models.CASCADE)
    class Meta:
        unique_together = (('itemName', 'size', 'itemGroup'),)
    
    def __str__(self):
        return self.itemName + " \t |ItemGroup:|" + str(self.itemGroup)

class Extras(models.Model):
    extra = models.CharField(max_length=30)
    price = models.FloatField()
    itemGroup = models.ForeignKey('ItemGroup', on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.extra + " \t |ItemGroup:|" + str(self.itemGroup)

class MenuItem(models.Model):
    itemGroup = models.ForeignKey('itemGroup', on_delete=models.CASCADE)
    item = models.CharField(max_length=30)
    extras = models.ManyToManyField(Extras, blank=True, related_name="topings")
    price = models.FloatField()