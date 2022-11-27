# Generated by Django 3.2.7 on 2022-07-01 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('taskapp', '0047_system_detail_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Store_password',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taskapp.user')),
            ],
        ),
    ]
