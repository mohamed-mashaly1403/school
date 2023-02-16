# Generated by Django 3.2.11 on 2023-02-12 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0041_auto_20230212_0335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='country',
            field=models.CharField(blank=True, choices=[('UAE', 'UAE-الإمارات'), ('KSA', 'السعودية-KSA'), ('Qatar', 'قطر-Qatar'), ('Kuwait', 'الكويت-Kuwait'), ('Egypt', 'مصر-Egypt')], default='General', max_length=30),
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