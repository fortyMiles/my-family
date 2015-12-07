from home.models import Home
from home.conf import default_home_pic


def create_home(owner, home_id):
    avatar = default_home_pic
    home = Home(owner=owner, home_id=home_id, avatar=avatar)
    home.save()


def update_home(data):
    pass

def get_home_info(home_id):
    pass

def get_joined_home_info(username):
    pass
