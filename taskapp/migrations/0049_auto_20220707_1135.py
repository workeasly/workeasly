# Generated by Django 3.2.7 on 2022-07-07 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskapp', '0048_store_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='Walk_in_Interviwee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('interviwer_name', models.CharField(blank=True, max_length=255, null=True)),
                ('profile', models.CharField(blank=True, max_length=255, null=True)),
                ('experience', models.CharField(blank=True, max_length=255, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('status', models.BooleanField(default=False)),
                ('cv', models.FileField(upload_to='cv')),
            ],
        ),
        migrations.AlterModelOptions(
            name='store_password',
            options={'verbose_name': 'Store Password'},
        ),
    ]