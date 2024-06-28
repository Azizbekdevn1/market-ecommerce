# Generated by Django 5.0.1 on 2024-05-01 14:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0011_order_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='district',
            options={'verbose_name': 'Tuman', 'verbose_name_plural': 'Tumanlar'},
        ),
        migrations.AlterModelOptions(
            name='region',
            options={'verbose_name': 'Viloyat', 'verbose_name_plural': 'Viloyatlar'},
        ),
        migrations.AddField(
            model_name='stream',
            name='view',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('yangi', 'Yangi'), ('yetkazildi', 'Yetkazildi'), ('arxivlandi', 'Arxivlandi'), ('yetkazilmoqda', 'Yetkazilmoqda'), ('nosoz_mahsulot', 'Nosoz maxsulot'), ('qaytib_keldi', 'Qaytib keldi'), ('bekor_qilindi', 'Bekor qilindi'), ('keyin_oladi', 'Keyin oladi'), ('dastavkaga_tayyor', 'Dastavkaga tayyor')], default='yangi', max_length=30),
        ),
        migrations.AlterField(
            model_name='order',
            name='stream',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='apps.stream'),
        ),
    ]
