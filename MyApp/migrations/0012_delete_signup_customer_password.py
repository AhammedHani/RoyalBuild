# Generated by Django 5.0.2 on 2024-02-28 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0011_signup_confirm_password_signup_password'),
    ]

    operations = [
        migrations.DeleteModel(
            name='signup',
        ),
        migrations.AddField(
            model_name='customer',
            name='password',
            field=models.CharField(default='123', max_length=100),
            preserve_default=False,
        ),
    ]