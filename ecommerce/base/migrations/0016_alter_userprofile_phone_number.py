# Generated by Django 4.2.5 on 2023-11-23 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_alter_userprofile_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='phone_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
