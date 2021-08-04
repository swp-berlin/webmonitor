# Generated by Django 3.1.4 on 2021-08-02 15:36

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swp', '0033_monitor_zotero_keys'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), blank=True, default=list, size=None, verbose_name='tags'),
        ),
    ]
