from django.db import models
import uuid

# Create your models here.


class Scope(models.Model):
    """
    Different privilage map to different feed groups.
    """
    SCOPE_TYPES = (
        ('home', 'is close family member'),
        ('relation', 'big family'),
        ('friend', 'friend'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    scope = models.CharField(max_length=30, unique=True)
    owner = models.CharField(max_length=13)
    tag = models.CharField(max_length=20, choices=SCOPE_TYPES)

    def is_home(self):
        return self.tag == 'home'

    def is_relation(self):
        return self.tag == 'relation'

    def is_friend(self):
        return self.tag == 'friend'

    class Meta:
        db_table = 'scope'


class ScopeGroup(models.Model):
    '''
    Puts different person into different scope
    '''
    SCOPE_TYPE = (
        ('home', 'is close family member'),
        ('relation', 'big family'),
        ('friend', 'friend'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    scope = models.CharField(max_length=30)
    member = models.CharField(max_length=13)
    create_time = models.DateTimeField(auto_now_add=True)
    tag = models.CharField(max_length=20, choices=SCOPE_TYPE, default='friend')

    class Meta:
        db_table = 'scope_group'
