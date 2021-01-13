# Generated by Django 3.1.4 on 2021-01-13 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swp', '0009_scraper_index_last_run'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monitor',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='active'),
        ),
        migrations.AlterField(
            model_name='scraper',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='active'),
        ),
        migrations.AlterField(
            model_name='thinktank',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='active'),
        ),
    ]
