# Generated by Django 4.1 on 2023-03-15 03:21

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_rename_date_created_on_document_date_updated_on_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='site_polygon',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, default=None, null=True, srid=4326),
        ),
    ]
