# Generated by Django 4.2.5 on 2024-02-03 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0003_services_alter_cake_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='services',
            name='image',
            field=models.ImageField(upload_to='services'),
        ),
    ]
