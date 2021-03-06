# Generated by Django 3.2.11 on 2022-01-12 01:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_alter_inbox_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inbox',
            name='order',
        ),
        migrations.AddField(
            model_name='inbox',
            name='is_receiver_delete',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='inbox',
            name='is_sender_delete',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='inbox',
            name='sender',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sentMessages', to=settings.AUTH_USER_MODEL),
        ),
    ]
