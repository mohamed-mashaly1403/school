# Generated by Django 3.2.11 on 2023-02-11 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_orderpoductclasses_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='changeteacherrequestt',
            name='type',
            field=models.CharField(default='other', max_length=100),
        ),
        migrations.AlterField(
            model_name='changeteacherrequestt',
            name='ip',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
