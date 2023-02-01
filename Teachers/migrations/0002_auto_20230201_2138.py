# Generated by Django 3.2.11 on 2023-02-01 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Teachers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacherprofile',
            name='BankCountry',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='teacherprofile',
            name='BankName',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='teacherprofile',
            name='Experience',
            field=models.TextField(blank=True, max_length=5000),
        ),
        migrations.AlterField(
            model_name='teacherprofile',
            name='Notes',
            field=models.TextField(blank=True, max_length=5000),
        ),
        migrations.AlterField(
            model_name='teacherprofile',
            name='city',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='teacherprofile',
            name='country',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='teacherprofile',
            name='grades',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='teacherprofile',
            name='qualifications1',
            field=models.CharField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='teacherprofile',
            name='qualifications2',
            field=models.CharField(blank=True, max_length=2000),
        ),
        migrations.AlterField(
            model_name='teacherprofile',
            name='qualifications3',
            field=models.CharField(blank=True, max_length=2000),
        ),
        migrations.AlterField(
            model_name='teacherprofile',
            name='qualifications4',
            field=models.CharField(blank=True, max_length=2000),
        ),
        migrations.AlterField(
            model_name='teacherprofile',
            name='specialzed_courses1',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='teacherprofile',
            name='specialzed_courses2',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='teacherprofile',
            name='specialzed_courses3',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]