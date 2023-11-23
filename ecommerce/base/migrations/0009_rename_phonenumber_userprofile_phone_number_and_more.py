# Generated by Django 4.2.5 on 2023-11-23 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_userprofile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='phoneNumber',
            new_name='phone_number',
        ),
        migrations.AddField(
            model_name='customer',
            name='phone_number',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_type',
            field=models.CharField(choices=[('customer', 'Customer'), ('seller', 'Seller'), ('admin', 'Admin')], max_length=20),
        ),
    ]
