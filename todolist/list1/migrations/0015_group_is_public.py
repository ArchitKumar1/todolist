# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-12-16 09:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list1', '0014_auto_20191216_0900'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='is_public',
            field=models.CharField(default='0', max_length=1),
        ),
    ]
