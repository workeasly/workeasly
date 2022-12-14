# Generated by Django 3.2.7 on 2022-05-27 12:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('taskapp', '0043_events'),
    ]

    operations = [
        migrations.CreateModel(
            name='Leave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leave_period', models.CharField(max_length=20)),
                ('leave_time', models.CharField(blank=True, max_length=20, null=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('leave_type', models.CharField(max_length=30)),
                ('leave_description', models.CharField(blank=True, max_length=100, null=True)),
                ('attendence', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='taskapp.attendence')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='taskapp.user')),
            ],
        ),
    ]
