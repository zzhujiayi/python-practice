# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-18 07:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='orer',
            new_name='order',
        ),
    ]
