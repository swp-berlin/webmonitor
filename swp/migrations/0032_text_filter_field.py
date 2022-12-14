# Generated by Django 3.1.4 on 2021-04-14 07:02

from django.db import migrations
import swp.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('swp', '0031_multiple_filter_values'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicationfilter',
            name='field',
            field=swp.models.fields.ChoiceField(choices=[('text', 'Text'), ('title', 'Title'), ('subtitle', 'Subtitle'), ('abstract', 'Abstract'), ('authors', 'Authors'), ('publication_date', 'Publication Date'), ('url', 'Url'), ('pdf_url', 'Pdf Url'), ('doi', 'Doi'), ('isbn', 'Isbn'), ('tags', 'Tags')], db_index=True, default='text', max_length=16, verbose_name='field'),
        ),
    ]
