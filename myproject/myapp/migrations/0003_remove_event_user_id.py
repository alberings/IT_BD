# Generated by Django 5.0.3 on 2024-04-23 23:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_event_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='user_id',
        ),
    ]