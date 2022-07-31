# Generated by Django 4.0 on 2021-12-28 09:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_course_is_school_subject'),
        ('orders', '0020_orderpoductclasses_classtime'),
    ]

    operations = [
        migrations.CreateModel(
            name='connect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
                ('orderd', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.orderpoduct')),
            ],
        ),
    ]
