# Generated by Django 5.1.1 on 2024-10-28 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_fertilizersingredients_measure_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pesticidebenefit',
            name='benefit',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='pesticidenotes',
            name='notes',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='pesticideusage',
            name='usage',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]