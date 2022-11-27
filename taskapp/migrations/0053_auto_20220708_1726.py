# Generated by Django 3.2.7 on 2022-07-08 11:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('taskapp', '0052_auto_20220708_1719'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event_photo',
            name='addevent',
        ),
        migrations.AddField(
            model_name='event_photo',
            name='addevent',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='taskapp.addevent'),
            preserve_default=False,
        ),
    ]
