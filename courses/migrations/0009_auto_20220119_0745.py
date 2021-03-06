# Generated by Django 3.2.11 on 2022-01-19 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_course_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_name_ar',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='course',
            name='course_name_en',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='course',
            name='description_ar',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='description_en',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='language1_ar',
            field=models.CharField(choices=[('Arabic', 'Arabic'), ('English', 'English'), ('French', 'French'), ('Chinese', 'Chinese')], default='', max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='language1_en',
            field=models.CharField(choices=[('Arabic', 'Arabic'), ('English', 'English'), ('French', 'French'), ('Chinese', 'Chinese')], default='', max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='language2_ar',
            field=models.CharField(choices=[('Arabic', 'Arabic'), ('English', 'English'), ('French', 'French'), ('Chinese', 'Chinese')], default='', max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='language2_en',
            field=models.CharField(choices=[('Arabic', 'Arabic'), ('English', 'English'), ('French', 'French'), ('Chinese', 'Chinese')], default='', max_length=15, null=True),
        ),
    ]
