# Generated by Django 5.1.2 on 2024-10-25 15:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0015_alter_user_role'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
