# Generated by Django 4.2.4 on 2023-08-26 04:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reqspec', '0014_usecase_project'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usecase',
            name='project',
        ),
        migrations.AddField(
            model_name='usecase',
            name='actor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='use_cases', to='reqspec.actor'),
            preserve_default=False,
        ),
    ]
