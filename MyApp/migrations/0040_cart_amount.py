# Generated by Django 5.0.2 on 2024-04-06 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0039_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='amount',
            field=models.CharField(default='90', max_length=100),
            preserve_default=False,
        ),
    ]
