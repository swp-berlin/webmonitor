# Generated by Django 3.1.4 on 2021-02-23 07:45

from django.db import migrations
import swp.models.fields
from swp.models.choices import ResolverType


def replace_old_author_config(config):
    if isinstance(config, list):
        for c in config:
            replace_old_author_config(c)

        return

    type = config.get('type')
    key = config.get('key')

    if type in [ResolverType.DATA, ResolverType.ATTRIBUTE, ResolverType.STATIC] and key == 'author':
        resolver = {**config, 'key': 'authors'}

        config.clear()

        config['type'] = ResolverType.AUTHORS
        config['resolver'] = resolver

        return

    if isinstance(config, dict):
        for k, v in config.items():
            if isinstance(v, (list, dict)):
                replace_old_author_config(v)


def migrate_authors(apps, schema_editor):
    PublicationFilter = apps.get_model('swp', 'PublicationFilter')
    Scraper = apps.get_model('swp', 'Scraper')

    PublicationFilter.objects.filter(field='author').update(field='authors')

    scrapers = Scraper.objects.all()

    for scraper in scrapers:
        replace_old_author_config(scraper.data)
        scraper.save()


class Migration(migrations.Migration):
    dependencies = [
        ('swp', '0015_publication_count_cached'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicationfilter',
            name='field',
            field=swp.models.fields.ChoiceField(
                choices=[('title', 'Title'), ('subtitle', 'Subtitle'), ('abstract', 'Abstract'),
                         ('authors', 'Authors'), ('publication_date', 'Publication Date'), ('url', 'URL'),
                         ('pdf_url', 'PDF URL')], db_index=True, default='title', max_length=16, verbose_name='field'),
        ),
        migrations.RunPython(code=migrate_authors, reverse_code=migrations.RunPython.noop),
    ]
