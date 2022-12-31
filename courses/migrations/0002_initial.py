# Generated by Django 3.2.11 on 2022-12-31 11:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0001_initial'),
        ('Teachers', '0001_initial'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ratingreview',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order'),
        ),
        migrations.AddField(
            model_name='ratingreview',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Teachers.teacherprofile'),
        ),
        migrations.AddField(
            model_name='course',
            name='type',
            field=models.ManyToManyField(blank=True, to='courses.Type'),
        ),
    ]
