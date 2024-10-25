# Generated by Django 5.1.2 on 2024-10-25 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0014_user_delete_teacher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('teacher', 'Teacher'), ('librarian', 'Librarian')], default='user', max_length=20),
        ),
    ]
