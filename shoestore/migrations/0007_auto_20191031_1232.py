# Generated by Django 2.2.6 on 2019-10-31 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoestore', '0006_item_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='quantity',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='quantity',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
