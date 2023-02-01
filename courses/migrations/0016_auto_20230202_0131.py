# Generated by Django 3.2.11 on 2023-02-01 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0015_auto_20230201_2302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='youtubeUrl',
            field=models.URLField(blank=True, null=True),
        ),
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
