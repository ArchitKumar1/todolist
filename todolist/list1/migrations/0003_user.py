# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-12-10 09:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list1', '0002_auto_20191209_1253'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userName', models.CharField(max_length=30)),
                ('userId', models.CharField(max_length=30)),
                ('userPassword', models.CharField(max_length=80)),
            ],
        ),
    ]
