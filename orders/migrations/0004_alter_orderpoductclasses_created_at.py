# Generated by Django 3.2.11 on 2023-02-10 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_orderpoductclasses_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderpoductclasses',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
