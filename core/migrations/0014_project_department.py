# Generated by Django 4.1 on 2023-03-16 10:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_project_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.department'),
        ),
    ]