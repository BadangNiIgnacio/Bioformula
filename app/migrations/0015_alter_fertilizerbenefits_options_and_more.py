# Generated by Django 5.1.1 on 2024-10-15 08:55

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_fertilizerbenefits_fertilizernotes'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fertilizerbenefits',
            options={'verbose_name_plural': 'Benefits'},
        ),
        migrations.AlterModelOptions(
            name='fertilizernotes',
            options={'verbose_name_plural': 'Notes'},
        ),
        migrations.CreateModel(
            name='PesticideBenefit',
            fields=[
                ('benefit_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('benefit', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.BooleanField(default=True)),
                ('pesticide', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app.pesticides')),
            ],
            options={
                'verbose_name_plural': 'Benefits',
            },
        ),
        migrations.CreateModel(
            name='PesticideNotes',
            fields=[
                ('notes_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('notes', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.BooleanField(default=True)),
                ('pesticide', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app.pesticides')),
            ],
            options={
                'verbose_name_plural': 'Notes',
            },
        ),
        migrations.CreateModel(
            name='PesticideUsage',
            fields=[
                ('usage_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('usage', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.BooleanField(default=True)),
                ('pesticide', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app.pesticides')),
            ],
            options={
                'verbose_name_plural': 'Usages',
            },
        ),
    ]
