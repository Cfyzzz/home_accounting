# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2020-03-13 15:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='controlmanager',
            old_name='managers',
            new_name='manager',
        ),
        migrations.RenameField(
            model_name='managercashitems',
            old_name='cash_items',
            new_name='cash_item',
        ),
    ]
