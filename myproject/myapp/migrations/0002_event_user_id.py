# Generated by Django 5.0.3 on 2024-04-23 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='user_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
