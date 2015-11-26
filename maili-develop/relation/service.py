"""
Data service of relation module

@author Minchiuan Gao<minchiuan.gao@gmail.com>
Build Date: 2015-Nov-25 Wed
"""

from .models import RelationValue
from .models import Relationship
from account.models import User
from .error import MyError


def check_user_exist(user):
    user = User.objects.filter(phone=user)
    if len(user) == 0:
        return False
    else:
        return True


def check_relation_exist(user1, user2):
    relation = User.objects.filter(user_from=user1, user_to=user2)

    if len(relation) == 0:
        return False
    else:
        return True


def check_relation_accept(relation):
    relation_dic = {}

    relation_value = RelationValue.objects.all()

    for relation in relation_value:
        relation_dic.setdefault(relation.title, True)

    if relation not in relation_dic:
        return False
    return True


def check_args(user1, user2, relation):
    try:
        check_user_exist(user1)
        check_user_exist(user2)
        check_relation_exist(user1, user2)
        check_relation_accept(relation)
    except Exception as e:
        raise e


def create_relation(user1, user2, relation, nickname):
    try:
        check_args(user1, user2, relation)
        new_relation = Relationship(
            user_from=user1, user_to=user2,
            relation=relation, nickname=nickname)
        new_relation.save()
        create_converse_relation(user1, user2, relation)
    except Exception as e:
        raise e


def create_converse_relation(user1, user2, relation):
    user1 =  User(phone=user1)
    pass
