# Generated by Django 4.0 on 2021-12-20 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_alter_order_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='quantity',
            field=models.IntegerField(blank=True, default=1),
        ),
    ]
