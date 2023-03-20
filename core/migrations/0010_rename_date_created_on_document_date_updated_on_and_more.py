# Generated by Django 4.1 on 2023-03-15 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_document_date_created_on'),
    ]

    operations = [
        migrations.RenameField(
            model_name='document',
            old_name='date_created_on',
            new_name='date_updated_on',
        ),
        migrations.AlterField(
            model_name='document',
            name='date_created',
            field=models.DateField(auto_now_add=True),
        ),
    ]
