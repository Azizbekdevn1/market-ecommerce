# Generated by Django 5.0.1 on 2024-03-26 16:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0003_alter_order_currier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='currier',
            field=models.ForeignKey(blank=True, limit_choices_to={'type': 'currier'}, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
