# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-12-11 10:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('list1', '0004_auto_20191210_1301'),
    ]

    operations = [
        migrations.CreateModel(
            name='Credentials',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(default='', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('group_id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('title', models.CharField(default='', max_length=30)),
            ],
        ),
        migrations.DeleteModel(
            name='Task',
        ),
        migrations.RemoveField(
            model_name='user',
            name='id',
        ),
        migrations.RemoveField(
            model_name='user',
            name='userId',
        ),
        migrations.RemoveField(
            model_name='user',
            name='userName',
        ),
        migrations.RemoveField(
            model_name='user',
            name='userPassword',
        ),
        migrations.AddField(
            model_name='user',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='user',
            name='user_id',
            field=models.CharField(default='', max_length=20, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='group',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='list1.User'),
        ),
        migrations.AddField(
            model_name='credentials',
            name='user_id',
            field=models.ForeignKey(default='', max_length=20, on_delete=django.db.models.deletion.CASCADE, to='list1.User'),
        ),
    ]
