# Generated by Django 3.2.11 on 2022-02-02 19:16

import Teachers.formatChecker
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Teachers', '0012_alter_paid_teacher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacherprofile',
            name='docfile',
            field=Teachers.formatChecker.ContentTypeRestrictedFileField(upload_to='cvs'),
        ),
    ]
