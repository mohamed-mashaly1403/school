# Generated by Django 4.0 on 2021-12-21 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_order_order_course_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='country',
            field=models.CharField(default='else', max_length=10),
        ),
    ]
