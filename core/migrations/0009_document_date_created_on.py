# Generated by Django 4.1 on 2023-03-15 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_document_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='date_created_on',
            field=models.DateField(auto_now=True),
        ),
    ]
