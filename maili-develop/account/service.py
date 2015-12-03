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
    import pdb; pdb.set_trace()
    data = create_avatar(data)
    user = User.objects.get(phone=data['phone'])
    serializer = UserSerializer(user, data=data)

    if serializer.is_valid():
        serializer.save()
    else:
        print serializer.errors


def create_new_user(data):
    data = create_avatar(data)
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        user_phone = data['phone']
        create_default_feed_group(user_phone)
        create_default_scope(user_phone)
    else:
        print serializer.errors


def create_avatar(data):
    if 'gender' in data and 'marital_status' in data:
        pic = get_avatar(data['gender'], data['marital_status'])
        data.setdefault('avatar', pic)
    return data


def get_avatar(gender, married):
    '''
    Set default avatar
    '''
    from account.configuration.picture import AVATAR

    picture = None
    import pdb;pdb.set_trace()

    married = married.lower()

    if married == 'false':
        married = False
    elif married == 'true':
        married = True

    if gender in AVATAR and married in AVATAR[gender]:
        picture = AVATAR[gender][married]
    else:
        picture = AVATAR['U']


    return picture
