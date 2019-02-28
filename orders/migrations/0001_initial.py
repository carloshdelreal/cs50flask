# Generated by Django 2.0.3 on 2019-02-21 14:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Extras',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('extra', models.CharField(max_length=30)),
                ('price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itemName', models.CharField(max_length=30)),
                ('price', models.FloatField()),
                ('size', models.CharField(blank=True, choices=[('', ''), ('sm', 'Small'), ('lg', 'Large')], default='', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='ItemGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itemGroup', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('placed_date', models.DateTimeField(auto_now=True)),
                ('placed', models.BooleanField()),
                ('delivered', models.BooleanField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SellingArticle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.CustomItem')),
                ('sell_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Topping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('toppingName', models.CharField(max_length=30)),
                ('price', models.FloatField(default=0.0)),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='itemGroup',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.ItemGroup'),
        ),
        migrations.AddField(
            model_name='customitem',
            name='extra',
            field=models.ManyToManyField(blank=True, to='orders.Extras'),
        ),
        migrations.AddField(
            model_name='customitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Item'),
        ),
        migrations.AddField(
            model_name='customitem',
            name='topping',
            field=models.ManyToManyField(blank=True, to='orders.Topping'),
        ),
        migrations.AddField(
            model_name='customitem',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='item',
            unique_together={('itemName', 'size', 'itemGroup')},
        ),
    ]