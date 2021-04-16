# Generated by Django 3.1.4 on 2021-03-19 11:44

import django.contrib.postgres.fields
from django.db import migrations, models

import swp.models.fields
import swp.models.thinktank
from swp.models.scraper import get_hash


def migrate_unique_field(apps, schema_editor):
    Thinktank = apps.get_model('swp', 'ThinkTank')

    for thinktank in Thinktank.objects.all():
        thinktank.unique_fields = [thinktank.unique_field]
        thinktank.save(update_fields=['unique_fields'])


def migrate_hash(apps, schema_editor):
    Publication = apps.get_model('swp', 'Publication')

    for publication in Publication.objects.all():
        publication.hash = get_hash({
            field: getattr(publication, field, '')
            for field in publication.thinktank.unique_fields
        })
        publication.save(update_fields=['hash'])


class Migration(migrations.Migration):

    dependencies = [
        ('swp', '0023_scrapererror_identifier'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='hash',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='hash'),
        ),
        migrations.AddField(
            model_name='thinktank',
            name='unique_fields',
            field=django.contrib.postgres.fields.ArrayField(base_field=swp.models.fields.ChoiceField(choices=[('url', 'URL'), ('title', 'Title')], db_index=True, default='url', max_length=5), default=swp.models.thinktank.get_default_unique_fields, size=None, verbose_name='unique fields'),
        ),
        migrations.RunPython(code=migrate_unique_field),
        migrations.RunPython(code=migrate_hash, reverse_code=migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='thinktank',
            name='unique_field',
        ),
    ]