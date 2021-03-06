# Generated by Django 4.0 on 2021-12-30 22:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Teachers', '0009_remove_teacherprofile_orders'),
        ('orders', '0027_complains'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderpoduct',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Teachers.teacherprofile'),
        ),
        migrations.AddField(
            model_name='orderpoductclasses',
            name='orders',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Teachers.teacherprofile'),
        ),
    ]
