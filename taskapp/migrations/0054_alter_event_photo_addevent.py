# Generated by Django 3.2.7 on 2022-07-11 05:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('taskapp', '0053_auto_20220708_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event_photo',
            name='addevent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='taskapp.addevent'),
        ),
    ]
