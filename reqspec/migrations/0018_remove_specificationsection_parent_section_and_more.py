# Generated by Django 4.2.4 on 2023-08-30 06:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reqspec', '0017_remove_usecase_specification_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='specificationsection',
            name='parent_section',
        ),
        migrations.RemoveField(
            model_name='specificationsection',
            name='title',
        ),
    ]
