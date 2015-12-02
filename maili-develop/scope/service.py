from scope.models import Scope
from scope.models import ScopeGroup
from relation.service import is_close_family_member
from group.group_service import create_home_group
from group.group_service import join_to_group
import time

FRIEND = 'friend'
HOME = 'home'
RELATION = 'relation'
SCOPES = [FRIEND, HOME, RELATION]


def create_one_scope(username, tag):
    '''
    By username and tag, creats a new scope
    '''
    scope_name = get_scope_name(username, tag)
    feed_group = Scope(scope=scope_name, owner=username, tag=tag)
    if tag == HOME:
        # set scope_name to this home group's id
        create_home_group(username, scope_name)
    feed_group.save()


def get_scope_name(username, tag):
    '''
    Based on username and tag, gives a unique scope name
    '''
    length = 8
    time_length = 5
    identity = username[length * (-1):]
    assic = str(ord(tag[-1]))
    time_str = str(time.time())[-1*time_length:].replace('.', '')
    scope_name = identity + time_str + assic
    return scope_name


def create_default_scope(username):
    '''
    Creates the default groups of each user.
    Each user has three groups, which is Global, Person Family, Big Family.
    '''
    for tag in SCOPES:
        create_one_scope(username, tag)


def update_user_scope(user1, user2, scope, relation):
    '''
    Adds user2 to user1's scope memeber.
    e.g
      user1 = 'BigHeadSon', user2 = 'HisMother', socpe = 'home'
      then add HisMother to BigHeadSon's Home Socpe Group
    '''
    scope_dict = {
        'H': HOME,
        'R': RELATION,
        'F': FRIEND
    }

    scope = scope_dict.get(scope)

    if scope == HOME:
        update_scope_group(user1, user2, HOME)

        home_id = get_home_id(user1)
        join_to_group(username=user2, group=home_id)
        # add user2 to user1's group home
        if is_close_family_member(user1, user2, relation):
            update_scope_group(user2, user1, HOME)

            home_id = get_home_id(user2)
            join_to_group(username=user1, group=home_id)
            # add user1 to user2's group home
        else:
            update_scope_group(user2, user1, RELATION)
    else:
        update_scope_group(user1, user2, scope)
        update_scope_group(user2, user1, scope)


def update_scope_group(user1, user2, tag):
    '''
    Add user2 to user1's scope member.
    '''
    scope = Scope.objects.filter(owner=user1).filter(tag=tag)[0].scope
    scope_group = ScopeGroup(scope=scope, member=user2, tag=tag)
    scope_group.save()


def get_home_member(user):
    '''
    Gets the 'seven' closet persons.
    '''
    scope_name = Scope.objects.filter(owner=user).filter(tag=HOME)[0].scope
    scope_member = ScopeGroup.objects.filter(scope=scope_name)

    user_json = {}

    for member in scope_member:
        user_json[member.member] = member.tag

    return user_json


def get_home_id(user):
    '''
    Gets the person's hoem id, for group chatting.
    '''
    scope_name = Scope.objects.filter(owner=user).filter(tag=HOME)[0].scope
    return scope_name
