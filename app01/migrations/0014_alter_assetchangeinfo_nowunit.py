# Generated by Django 4.0.6 on 2024-04-14 08:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0013_assetchangeinfo_confirmed_assetdamageinfo_confirmed_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetchangeinfo',
            name='NowUnit',
            field=models.ForeignKey(max_length=16, on_delete=django.db.models.deletion.CASCADE, related_name='asset_change_NowUnit', to='app01.department', verbose_name='原使用单位'),
        ),
    ]