# Generated by Django 4.0 on 2021-12-31 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Teachers', '0011_paid'),
        ('orders', '0028_orderpoduct_teacher_orderpoductclasses_orders'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderpoduct',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Teachers.teacherprofile'),
        ),
    ]
