# Generated by Django 3.1.3 on 2022-03-21 05:42

import companies.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0004_auto_20220227_2054'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='id',
        ),
        migrations.AlterField(
            model_name='device',
            name='deviceID',
            field=models.CharField(default=companies.models.UniqueID, editable=False, max_length=7, primary_key=True, serialize=False),
        ),
    ]
