# Generated by Django 2.0.3 on 2018-12-23 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20181222_2113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='size',
            field=models.CharField(blank=True, choices=[('', ''), ('sm', 'Small'), ('lg', 'Large')], default='', max_length=20),
        ),
    ]
