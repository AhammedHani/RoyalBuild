# Generated by Django 5.0.2 on 2024-02-26 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0003_staff'),
    ]

    operations = [
        migrations.CreateModel(
            name='vehicle',
            fields=[
                ('vehicle_id', models.IntegerField(primary_key=True, serialize=False)),
                ('vehicle_number', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'vehicle',
            },
        ),
    ]