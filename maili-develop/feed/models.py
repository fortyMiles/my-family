from django.db import models
import uuid

# Create your models here.


class FeedGroup(models.Model):
    """
    Different privilage map to different feed groups.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group_id = models.CharField(max_length=30, unique=True)
    creator = models.CharField(max_length=13)
    tag = models.CharField(max_length=20)

    class Meta:
        db_table = 'feed_group'
