# Generated by Django 3.1.4 on 2021-02-04 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swp', '0012_publication_filter'),
    ]

    operations = [
        migrations.AddField(
            model_name='monitor',
            name='description',
            field=models.TextField(blank=True, verbose_name='description'),
        ),
    ]
