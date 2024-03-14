# Generated by Django 5.0.2 on 2024-02-27 06:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0006_customer_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='CUSTOMER',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='MyApp.customer'),
        ),
        migrations.AddField(
            model_name='review',
            name='CUSTOMER',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='MyApp.customer'),
        ),
    ]
