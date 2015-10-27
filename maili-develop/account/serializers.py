from account.models import User
from account.models import Friendship
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone', 'password', 'last_name')


class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = ('friend_name', 'friend_phone', 'remark_name', 'first_char', 'remark_tags', 'send_msg_count', 'receive_msg_count', 'unread_msgs', 'deleted')
