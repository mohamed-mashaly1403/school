# Generated by Django 4.0 on 2021-12-25 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0014_remove_orderpoduct_class_url_orderpoduct_is_deliverd_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
