from group.models import Group
from group.models import UserGroups
from group.serializers import HomeInfoSerializer
from group.serializers import JoinedGroupsSerializer
from group.conf import default_home_pic
from relation.service import get_chinese_relation
import time


def get_join_home_info(username, home_list):
    data_list = []
    for home in home_list:
        data = get_home_info(home)
        temp = {}
        temp['id'] = home
        temp['avatar'] = '2211f3027e6e682361c552cd6c721e08.png'
        temp['nickname'] = get_chinese_relation(username, data['creator'])
        data_list.append(temp)
    return data_list

def get_home_info(group_id):
    home = Group.objects.filter(name=group_id)[0]
    serializer = HomeInfoSerializer(home)
    data = serializer.data
    return data



def group_exist(group_name):
    query_set = Group.objects.all().filter(name=group_name)
    if query_set.exists():
        return True
    else:
        return False


def create_home_group(creator, home_id):
    group = Group(name=home_id, creator=creator, type='H')
    group.save()


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
