# Generated by Django 4.1 on 2023-03-27 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_projectsite'),
    ]

    operations = [
        migrations.CreateModel(
            name='SystemSummary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('month', models.IntegerField()),
                ('total_projects', models.IntegerField(default=0)),
                ('total_users', models.IntegerField(default=0)),
            ],
            options={
                'unique_together': {('year', 'month')},
            },
        ),
    ]
