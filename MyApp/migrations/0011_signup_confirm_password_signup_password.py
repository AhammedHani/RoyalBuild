# Generated by Django 5.0.2 on 2024-02-28 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0010_remove_signup_confirm_password_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='signup',
            name='confirm_password',
            field=models.CharField(default=123, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='signup',
            name='password',
            field=models.CharField(default=123, max_length=100),
            preserve_default=False,
        ),
    ]