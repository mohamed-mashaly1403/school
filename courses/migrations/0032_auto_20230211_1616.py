# Generated by Django 3.2.11 on 2023-02-11 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0031_auto_20230211_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='price',
            name='CprivAR',
            field=models.ManyToManyField(blank=True, to='courses.CoursePrevAR'),
        ),
        migrations.AlterField(
            model_name='price',
            name='CprivEN',
            field=models.ManyToManyField(blank=True, to='courses.CoursePrevEN'),
        ),
    ]
