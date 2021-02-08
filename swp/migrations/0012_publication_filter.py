# Generated by Django 3.1.4 on 2021-02-04 07:41

from django.db import migrations, models
import django.db.models.deletion
import swp.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('swp', '0011_publication_authors_max_length_255'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thinktankfilter',
            name='query',
        ),
        migrations.CreateModel(
            name='PublicationFilter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field', swp.models.fields.ChoiceField(choices=[('title', 'Title'), ('subtitle', 'Subtitle'), ('abstract', 'Abstract'), ('author', 'Author'), ('publication_date', 'Publication Date'), ('url', 'URL'), ('pdf_url', 'PDF URL')], db_index=True, default='title', max_length=16, verbose_name='field')),
                ('comparator', swp.models.fields.ChoiceField(choices=[('contains', 'Contains'), ('starts_with', 'Starts With'), ('ends_with', 'Ends With')], db_index=True, default='contains', max_length=11, verbose_name='comparator')),
                ('value', models.CharField(max_length=255, verbose_name='value')),
                ('thinktank_filter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='publication_filters', to='swp.thinktankfilter', verbose_name='think tank filter')),
            ],
            options={
                'verbose_name': 'publication filter',
                'verbose_name_plural': 'publication filters',
            },
        ),
    ]