# Generated by Django 3.2.7 on 2021-12-28 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('taskapp', '0009_remove_multiple_select_language_type_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='multiple_select_language',
            name='task_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='taskapp.tasktype'),
        ),
    ]