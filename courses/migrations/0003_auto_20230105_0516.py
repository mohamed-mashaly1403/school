# Generated by Django 3.2.11 on 2023-01-05 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='type',
            old_name='tybe_Type',
            new_name='tybe_Type_en',
        ),
        migrations.AddField(
            model_name='type',
            name='tybe_Type_ar',
            field=models.CharField(default='', max_length=30),
        ),
    ]
