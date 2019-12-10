# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Item(models.Model):
    task  = models.CharField(max_length=5000)
    itemid = models.CharField(max_length=50)
    checkstatus = models.CharField(max_length=40)


