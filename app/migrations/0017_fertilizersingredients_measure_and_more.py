# Generated by Django 5.1.1 on 2024-10-15 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_pesticidetargetpest'),
    ]

    operations = [
        migrations.AddField(
            model_name='fertilizersingredients',
            name='measure',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='pesticideingredients',
            name='measure',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
