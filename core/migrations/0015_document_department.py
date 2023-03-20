# Generated by Django 4.1 on 2023-03-17 06:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_project_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.department'),
        ),
    ]