# Generated by Django 4.2.4 on 2023-08-25 15:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reqspec', '0012_remove_staff_actors_actor_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='project',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='staff', to='reqspec.project'),
            preserve_default=False,
        ),
    ]
