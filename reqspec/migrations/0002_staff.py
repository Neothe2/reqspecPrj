# Generated by Django 4.2 on 2023-08-03 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reqspec', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=255)),
                ('actors', models.ManyToManyField(to='reqspec.actor')),
            ],
        ),
    ]
