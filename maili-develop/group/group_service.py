from group.models import Group
from group.models import UserGroups
from account.models import User
from group.serializers import GroupSerializer
from group.serializers import JoinedGroupsSerializer
import time


def group_exist(group_name):
    query_set = Group.objects.all().filter(name=group_name)
    if query_set.exists():
        return True
    else:
        return False


def create_group(creator, category='H'):
    group_name = create_group_name(creator)
    group = Group(name=group_name, creator=creator, type=category)
    group.save()
    return group_name


def create_group_name(creator):
    length = 8
    time_length = 13
    identity = creator[length*-1:]
    time_str = str(time.time())[:time_length].replace('.', '')
    return identity + time_str


def join_to_group(username, group):
    new_join = UserGroups(user=username, group=group)
    new_join.save()


def get_member_joined_groups(username):
    result_set = UserGroups.objects.filter(user=username).values('group')
    serializer = JoinedGroupsSerializer(result_set, many=True)
    return serializer.data
