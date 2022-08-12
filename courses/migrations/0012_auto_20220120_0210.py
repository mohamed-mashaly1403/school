# Generated by Django 3.2.11 on 2022-01-19 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_alter_course_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='language1_tr',
            field=models.CharField(choices=[('Arabic', 'Arabic'), ('English', 'English'), ('French', 'French'), ('Chinese', 'Chinese')], default='', max_length=15),
        ),
        migrations.AddField(
            model_name='course',
            name='language2_tr',
            field=models.CharField(choices=[('Arabic', 'Arabic'), ('English', 'English'), ('French', 'French'), ('Chinese', 'Chinese')], default='', max_length=15),
        ),
    ]