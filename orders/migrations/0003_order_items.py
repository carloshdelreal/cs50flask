# Generated by Django 2.0.3 on 2019-02-22 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_item_customizable'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(through='orders.SellingArticle', to='orders.CustomItem'),
        ),
    ]