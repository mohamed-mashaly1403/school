# Generated by Django 4.0 on 2022-01-04 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_inbox_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inbox',
            name='order',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
