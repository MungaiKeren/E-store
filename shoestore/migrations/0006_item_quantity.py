# Generated by Django 2.2.6 on 2019-10-31 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoestore', '0005_item_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='quantity',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
