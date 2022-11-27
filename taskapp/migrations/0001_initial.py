# Generated by Django 3.2.7 on 2021-12-14 04:33

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import taskapp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projectapp', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('office_user_id', models.CharField(blank=True, max_length=255, null=True)),
                ('reporting_to', models.CharField(blank=True, max_length=50, null=True)),
                ('is_employee', models.BooleanField(default=False)),
                ('profile_updated', models.BooleanField(default=False)),
                ('display_pic', models.ImageField(blank=True, null=True, upload_to=taskapp.models.get_upload_path)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ProgrammingLanguage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_name', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Languages / Department',
            },
        ),
        migrations.CreateModel(
            name='system_detail',
            fields=[
                ('system_type', models.CharField(choices=[('Computer', 'Computer'), ('Laptop', 'Laptop'), ('Macbook', 'MacBook')], max_length=255)),
                ('specification', models.TextField()),
                ('system_service', models.TextField(blank=True, null=True)),
                ('system_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('added_on', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'System Detail',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('details', models.TextField()),
                ('added_on', models.DateTimeField()),
                ('updated_on', models.DateTimeField(blank=True, null=True)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projectapp.project')),
            ],
            options={
                'verbose_name': 'Task',
            },
        ),
        migrations.CreateModel(
            name='TaskType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('for_all', models.BooleanField(default=False)),
                ('programming_language', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='taskapp.programminglanguage')),
            ],
            options={
                'verbose_name': 'Task Type',
            },
        ),
        migrations.CreateModel(
            name='task_uploaded_file',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaded_file', models.FileField(upload_to=taskapp.models.get_upload_files_path)),
                ('extension', models.CharField(max_length=255)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taskapp.task')),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='task_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taskapp.tasktype'),
        ),
        migrations.AddField(
            model_name='task',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taskapp.user'),
        ),
        migrations.CreateModel(
            name='Assigned_System_Detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_type', models.CharField(choices=[('Temporary', 'Temporary'), ('Permanent', 'Permanent')], max_length=255)),
                ('assigned_on', models.DateTimeField()),
                ('returned_on', models.DateTimeField(blank=True, null=True)),
                ('system_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='taskapp.system_detail')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='taskapp.user')),
            ],
            options={
                'verbose_name': 'Assigned System Detail',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='programming_language',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='taskapp.programminglanguage'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]