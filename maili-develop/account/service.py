from account.models import User
from .serializers import UserSerializer
from feed.service import create_default_feed_group


def user_exist(username):
    user = User.objects.filter(phone=username)
    if user:
        return True
    else:
        return False


def update_user(data):
    user = User.objects.get(phone=data['phone'])
    serializer = UserSerializer(user, data=data)

    if serializer.is_valid():
        serializer.save()
    else:
        print serializer.errors


def create_new_user(data):
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        create_default_feed_group(data['phone'])
    else:
        print serializer.errors
