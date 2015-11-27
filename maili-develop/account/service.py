from account.models import User
from .serializers import UserSerializer
from feed.service import create_default_feed_group
from scope.service import create_default_scope


def get_user(phone_number):
    user_set = User.objects.filter(phone=phone_number)
    if len(user_set) > 0:
        return user_set[0]
    else:
        return None


def user_has_married(phone_number):
    user = get_user(phone_number)
    return user.marital_status


def get_user_info(username):
    user = get_user(username)
    if user:
        serializer = UserSerializer(user)
        return serializer.data
    else:
        return None


def check_user_exist(username):
    user_set = User.objects.filter(phone=username)
    if len(user_set) == 0:
        return False
    else:
        return True


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
        user_phone = data['phone']
        create_default_feed_group(user_phone)
        create_default_scope(user_phone)
    else:
        print serializer.errors
