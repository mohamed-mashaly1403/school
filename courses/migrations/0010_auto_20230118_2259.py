# Generated by Django 3.2.11 on 2023-01-18 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_auto_20230117_0113'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoursePrevARNaa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('privArNa', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='CoursePrevENNa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('privEnNa', models.CharField(max_length=30)),
            ],
        ),
        migrations.RenameField(
            model_name='courseprevar',
            old_name='priv_ar',
            new_name='privAr',
        ),
        migrations.RenameField(
            model_name='coursepreven',
            old_name='priv_en',
            new_name='privEn',
        ),
        migrations.RenameField(
            model_name='price',
            old_name='privAR',
            new_name='CprivAR',
        ),
        migrations.RenameField(
            model_name='price',
            old_name='privEN',
            new_name='CprivEN',
        ),
        migrations.AddField(
            model_name='price',
            name='courseClasses_Ar',
            field=models.CharField(default='واحد', max_length=30),
        ),
        migrations.AddField(
            model_name='price',
            name='courseClasses_En',
            field=models.CharField(default='one', max_length=30),
        ),
        migrations.AlterField(
            model_name='price',
            name='CprivAR',
            field=models.ManyToManyField(blank=True, to='courses.CoursePrevAR'),
        ),
        migrations.AlterField(
            model_name='price',
            name='CprivEN',
            field=models.ManyToManyField(blank=True, to='courses.CoursePrevEN'),
        ),
        migrations.AddField(
            model_name='price',
            name='CprivARNa',
            field=models.ManyToManyField(blank=True, to='courses.CoursePrevARNaa'),
        ),
        migrations.AddField(
            model_name='price',
            name='CprivENNa',
            field=models.ManyToManyField(blank=True, to='courses.CoursePrevENNa'),
        ),
    ]
