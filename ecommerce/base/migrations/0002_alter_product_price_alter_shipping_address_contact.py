# Generated by Django 4.2.5 on 2023-09-21 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name="shipping_address",
            name="contact",
            field=models.IntegerField(),
        ),
    ]
