# Generated by Django 3.2.7 on 2022-01-24 11:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taskapp', '0020_auto_20220121_1703'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reporting',
            old_name='user_from',
            new_name='existing_reporting_to',
        ),
        migrations.RenameField(
            model_name='reporting',
            old_name='user_to',
            new_name='new_reporting_to',
        ),
    ]
