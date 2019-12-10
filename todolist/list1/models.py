# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Task(models.Model):
    taskDescription  = models.CharField(max_length=200)
    taskId = models.CharField(max_length=50)
    taskGroupId = models.CharField(max_length=50)
    taskStatus = models.BooleanField()


class User(models.Model):
    userName = models.CharField(max_length=30)
    userId = models.CharField(max_length=30)
    userPassword = models.CharField(max_length=80)


