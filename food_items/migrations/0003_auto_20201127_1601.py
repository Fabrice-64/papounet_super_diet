# Generated by Django 3.1.2 on 2020-11-27 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food_items', '0002_auto_20201112_0653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bestproductselection',
            name='date_selection',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]