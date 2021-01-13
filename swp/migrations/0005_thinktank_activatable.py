# Generated by Django 3.1.4 on 2020-12-04 11:17

from django.db import migrations, models
import swp.models.abstract


class Migration(migrations.Migration):

    dependencies = [
        ('swp', '0004_scraper_changes'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='thinktank',
            managers=[
                ('objects', swp.models.abstract.ActivatableManager()),
            ],
        ),
        migrations.AddField(
            model_name='thinktank',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='active'),
        ),
    ]
