# Generated by Django 4.0 on 2021-12-28 23:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_course_is_school_subject'),
        ('orders', '0022_remove_connect_course_connect_course_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='connector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
                ('op', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.orderpoduct')),
            ],
        ),
        migrations.DeleteModel(
            name='connect',
        ),
    ]
