# Generated by Django 5.0.1 on 2024-02-23 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0003_basemodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='count',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
