# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class User(models.Model):
    name = models.CharField(max_length = 20,default="")
    user_id = models.CharField(max_length = 20,primary_key=True,default="")
    password = models.CharField(max_length=20, default="")
    active = models.BooleanField(default=True)


class Group(models.Model):
    group_id = models.CharField(max_length=30,primary_key=True)
    title = models.CharField(max_length=30,default="")
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)

class Task(models.Model):

    task_id = models.CharField(max_length=50,primary_key=True,default="")
    description  = models.CharField(max_length=200,default="")
    status = models.BooleanField(default=True)
    group_id = models.ForeignKey(Group,on_delete=models.CASCADE)




