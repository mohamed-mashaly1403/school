# Generated by Django 3.2.11 on 2022-12-31 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=50, unique=True)),
                ('course_name_ar', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('slug', models.CharField(max_length=100, unique=True)),
                ('language1', models.CharField(choices=[('Arabic', 'Arabic'), ('English', 'English'), ('French', 'French'), ('Chinese', 'Chinese')], default='', max_length=15)),
                ('language1_tr', models.CharField(choices=[('العربية', 'العربية'), ('الإنجليزية', 'الإنجليزية'), ('الفرنسية', 'الفرنسية'), ('الصينية', 'الصينية')], default='', max_length=15)),
                ('language2', models.CharField(choices=[('Arabic', 'Arabic'), ('English', 'English'), ('French', 'French'), ('Chinese', 'Chinese')], default='', max_length=15)),
                ('language2_tr', models.CharField(choices=[('العربية', 'العربية'), ('الإنجليزية', 'الإنجليزية'), ('الفرنسية', 'الفرنسية'), ('الصينية', 'الصينية')], default='', max_length=15)),
                ('description', models.TextField(blank=True, max_length=500)),
                ('description_ar', models.TextField(blank=True, max_length=500, null=True)),
                ('img', models.ImageField(blank=True, upload_to='img/courses')),
                ('is_school_subject', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tybe_Type', models.CharField(max_length=30)),
            ],
        ),
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
            ],
        ),
    ]
