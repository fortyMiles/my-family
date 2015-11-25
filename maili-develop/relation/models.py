# -*- coding:utf-8 -*-
from django.db import models


class RelationValue(models.Model):
    title = models.CharField(max_length=10)
    weight = models.IntegerField()
    abbr = models.CharField(max_length=10)
    level = models.IntegerField()
    cft = models.CharField(max_length=10)
    cfa = models.CharField(max_length=10)
    cmt = models.CharField(max_length=10)
    cma = models.CharField(max_length=10)


class Relationship(models.Model):
    user_from = models.CharField(max_length=15)
    user_to = models.CharField(max_length=15)
    relation = models.CharField(max_length=15)
    nicknam = models.CharField(max_length=15)
    create_at = models.DateTimeField(auto_now_add=True)
