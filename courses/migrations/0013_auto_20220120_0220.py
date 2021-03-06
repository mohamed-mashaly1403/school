# Generated by Django 3.2.11 on 2022-01-19 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0012_auto_20220120_0210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='language1_tr',
            field=models.CharField(choices=[('Arabic', 'العربية'), ('English', 'الإنجليزية'), ('French', 'الفرنسية'), ('Chinese', 'الصينية')], default='', max_length=15),
        ),
        migrations.AlterField(
            model_name='course',
            name='language2_tr',
            field=models.CharField(choices=[('Arabic', 'العربية'), ('English', 'الإنجليزية'), ('French', 'الفرنسية'), ('Chinese', 'الصينية')], default='', max_length=15),
        ),
    ]
