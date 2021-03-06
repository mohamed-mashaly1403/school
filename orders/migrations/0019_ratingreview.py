# Generated by Django 4.0 on 2021-12-27 03:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_course_is_school_subject'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0018_orderpoductclasses_class_url_is_deliverd'),
    ]

    operations = [
        migrations.CreateModel(
            name='RatingReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(blank=True, max_length=100)),
                ('review', models.TextField(blank=True, max_length=500)),
                ('rating', models.FloatField()),
                ('ip', models.CharField(blank=True, max_length=20)),
                ('status', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
