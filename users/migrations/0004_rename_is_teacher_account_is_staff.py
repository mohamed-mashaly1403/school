# Generated by Django 4.0 on 2021-12-13 18:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_rename_is_staff_account_is_teacher'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='is_teacher',
            new_name='is_staff',
        ),
    ]
