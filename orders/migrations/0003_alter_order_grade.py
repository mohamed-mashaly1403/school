# Generated by Django 4.0 on 2021-12-15 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_remove_order_classes_remove_order_order_course_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='grade',
            field=models.IntegerField(blank=True, default=1),
        ),
    ]
