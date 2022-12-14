# Generated by Django 3.1.2 on 2020-11-26 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swp', '0002_basic_models'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monitor',
            name='interval',
            field=models.PositiveIntegerField(choices=[(12, 'twice daily'), (24, 'daily'), (168, 'weekly'), (5040, 'monthly')], default=24, verbose_name='interval'),
        ),
        migrations.AlterField(
            model_name='scraper',
            name='interval',
            field=models.PositiveIntegerField(choices=[(12, 'twice daily'), (24, 'daily'), (168, 'weekly'), (5040, 'monthly')], default=24, verbose_name='interval'),
        ),
    ]
