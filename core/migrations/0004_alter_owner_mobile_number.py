# Generated by Django 4.1 on 2023-03-14 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_project_time_started'),
    ]

    operations = [
        migrations.AlterField(
            model_name='owner',
            name='mobile_number',
            field=models.CharField(max_length=10),
        ),
    ]
