# Generated by Django 4.2.5 on 2024-02-03 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cake',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]