# Generated by Django 4.0 on 2021-12-26 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0016_orderpoductclasses_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderpoductclasses',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='orderpoductclasses',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
