# Generated by Django 3.2.11 on 2022-02-05 18:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('live', '0002_auto_20220204_2248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='closelive',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
