# Generated by Django 5.1.3 on 2024-12-23 01:11

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('espdata', '0002_sensordata_node'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensordata',
            name='node',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='sensordata',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]