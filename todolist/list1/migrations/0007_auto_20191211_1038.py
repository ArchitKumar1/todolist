# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-12-11 10:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('list1', '0006_task'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='id',
            new_name='task_id',
        ),
    ]
