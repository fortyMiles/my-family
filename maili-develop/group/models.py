from django.db import models
import uuid

# Create your models here.


class Group(models.Model):
    '''
    Defines the group information.
    '''

    TYPE = (
        ('F', 'freinds'),
        ('H', 'home'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, unique=True)
    # each group has an unique name, like account name for a person.
    creator = models.CharField(max_length=13)
    nickname = models.CharField(max_length=20)
    create_time = models.DateTimeField(auto_now=True)
    member_number = models.IntegerField(default=1)
    slogen = models.CharField(max_length=100)
    type = models.CharField(max_length=2, choices=TYPE)

    class Meta:
        db_table = 'group'


class UserGroups(models.Model):
    '''
    define the user-group information.
    '''
    user = models.CharField(max_length=30, default='null')
    group = models.CharField(max_length=30, default='null')
    create_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_groups'
