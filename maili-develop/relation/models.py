from django.db import models
import uuid

# Create your models here.


class RelationValue(models.Model):
    title = models.CharField(max_length=10)
    weight = models.IntegerField()
    abbr = models.CharField(max_length=4)
    level = models.IntegerField()
    cft = models.CharField(max_length=4)  # converse female title
    cfa = models.CharField(max_length=4)  # converse female abbr
    cmt = models.CharField(max_length=4)  # converse male title
    cma = models.CharField(max_length=4)  # converse male abbr

    class Meta:
        db_table = 'relation_value'


class Relationship(models.Model):
    from_user_id = models.UUIDField(db_index=True)
    to_user_id = models.UUIDField(db_index=True)
    relation = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    nickname = models.CharField(max_length=15)

    class Meta:
        db_table = "relationship"


