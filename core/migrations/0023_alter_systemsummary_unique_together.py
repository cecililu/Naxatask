# Generated by Django 4.1 on 2023-03-28 09:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_alter_systemsummary_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='systemsummary',
            unique_together=set(),
        ),
    ]