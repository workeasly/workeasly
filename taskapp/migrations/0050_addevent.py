# Generated by Django 3.2.7 on 2022-07-08 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskapp', '0049_auto_20220707_1135'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25)),
                ('created_at', models.DateField(auto_now=True)),
                ('event_date', models.DateField()),
                ('description', models.CharField(max_length=240)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='event_images')),
            ],
        ),
    ]
