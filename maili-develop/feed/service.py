from feed.models import FeedGroup
import time


def create_feed_group(username, tag):
    '''
    By username and tag, creats a new group feed.
    '''
    group_id = get_feed_group_name(username, tag)
    feed_group = FeedGroup(group_id=group_id, creator=username, tag=tag)
    feed_group.save()


def get_feed_group_name(username, tag):
    length = 8
    time_length = 5
    identity = username[length * (-1):]
    assic = str(ord(tag[-1]))
    time_str = str(time.time())[-1*time_length:].replace('.', '')
    feed_group = identity + time_str + assic
    return feed_group


def create_default_feed_group(username):
    '''
    Creates the default groups of each user.
    Each user has three groups, which is Global, Person Family, Big Family.
    '''
    defaults = ['global', 'home', 'family']
    for tag in defaults:
        create_feed_group(username, tag)
