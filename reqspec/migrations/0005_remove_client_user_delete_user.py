# Generated by Django 4.2.4 on 2023-08-03 14:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reqspec', '0004_user_client_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='user',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
