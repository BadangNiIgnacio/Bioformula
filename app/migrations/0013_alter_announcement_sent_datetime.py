# Generated by Django 5.1.1 on 2024-10-15 06:05

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_alter_appointments_options_alter_uom_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='sent_datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
