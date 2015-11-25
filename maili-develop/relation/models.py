# -*- coding:utf-8 -*-
from django.db import models


class RelationValue(models.Model):
    title = models.CharField(max_length=10)
    weight = models.IntegerField()
    abbr = models.CharField(max_length=10)
    level = models.IntegerField()
    cft = models.CharField(max_length=10)
    cfa = models.IntegerField()
    cmt = models.CharField(max_length=10)
    cma = models.IntegerField()
