from rest_framework import serializers

from group.models import Group
from group.models import UserGroups


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        field = ('name', 'creator', 'nickname',
                 'member_number', 'slogen', 'type')


class JoinedGroupsSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserGroups
        field = ('group')
