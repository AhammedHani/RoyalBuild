# Generated by Django 5.0.2 on 2024-03-25 07:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0026_rename_remark_worksite_remark'),
    ]

    operations = [
        migrations.RenameField(
            model_name='worksite',
            old_name='Photo1',
            new_name='photo1',
        ),
        migrations.RenameField(
            model_name='worksite',
            old_name='Photo2',
            new_name='photo2',
        ),
        migrations.RenameField(
            model_name='worksite',
            old_name='Photo3',
            new_name='photo3',
        ),
    ]
