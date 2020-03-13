# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2020-03-13 15:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cashitem', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashitem',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Период'),
        ),
        migrations.AlterField(
            model_name='cashitem',
            name='min_value',
            field=models.IntegerField(default=0, verbose_name='Минимальный порог'),
        ),
        migrations.AlterField(
            model_name='cashitem',
            name='plan_value',
            field=models.IntegerField(default=0, verbose_name='Плановое значение'),
        ),
        migrations.AlterField(
            model_name='cashitem',
            name='value',
            field=models.IntegerField(default=0, verbose_name='Значение'),
        ),
        migrations.AlterField(
            model_name='cashitem',
            name='virtual_value',
            field=models.IntegerField(default=0, verbose_name='Плановый приход'),
        ),
    ]