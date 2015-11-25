from django.db import models

# Create your models here.

class RelationValue(models.Model):
    title = models.CharField(max_length=10)
    weight = models.IntegerField()
    abbr = models.CharField(max_length=4)
    level = models.IntegerField()
