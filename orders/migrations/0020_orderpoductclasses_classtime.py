# Generated by Django 4.0 on 2021-12-27 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0019_ratingreview'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderpoductclasses',
            name='classTime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]