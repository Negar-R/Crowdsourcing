# Generated by Django 2.2 on 2020-11-30 08:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_taskmodel_estimation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskmodel',
            name='assignee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assignees', to=settings.AUTH_USER_MODEL),
        ),
    ]
