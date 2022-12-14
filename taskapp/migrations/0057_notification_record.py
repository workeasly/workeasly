# Generated by Django 3.2.7 on 2022-07-20 09:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('taskapp', '0056_store_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification_record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now=True)),
                ('status', models.CharField(max_length=240)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='taskapp.user')),
            ],
        ),
    ]
