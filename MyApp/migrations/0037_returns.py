# Generated by Django 5.0.2 on 2024-04-04 07:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0036_scheduler'),
    ]

    operations = [
        migrations.CreateModel(
            name='returns',
            fields=[
                ('returns_id', models.IntegerField(primary_key=True, serialize=False)),
                ('date', models.CharField(max_length=100)),
                ('reason', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
                ('ORDER', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='MyApp.make_order')),
            ],
            options={
                'db_table': 'returns',
            },
        ),
    ]
