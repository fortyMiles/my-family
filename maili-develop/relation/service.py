# -*- coding: utf-8 -*-
"""
Data service of relation module

@author Minchiuan Gao<minchiuan.gao@gmail.com>
Build Date: 2015-Nov-25 Wed
"""
from .models import RelationValue
from .models import Relationship
from account.models import User
from .models import Contract
from .serializers import ContractSerilizer


def check_user_exist(user):
    user = User.objects.filter(phone=user)
    if len(user) == 0:
        return False
    else:
        return True


def check_relation_exist(user1, user2):
    '''
    check if there already is an existed relation between two persons.
    '''
    relation = Relationship.objects.filter(user_from=user1, user_to=user2)

    if len(relation) == 0:
        return False
    else:
        return True


def check_relation_accept(relation):
    '''
    Checks if this relation is included on the existed realtions.
    '''
    relation_set = RelationValue.objects.filter(title=relation)

    if len(relation_set) > 0:
        return True
    else:
        return False


def check_args(user1, user2, relation):
    check_user_exist(user1)
    check_user_exist(user2)
    check_relation_exist(user1, user2)
    check_relation_accept(relation)


def create_relation(user1, user2, relation, nickname):
    abbr = RelationValue.objects.filter(title=relation)[0].abbr

    new_relation = Relationship(
        user_from=user1, user_to=user2,
        relation=abbr, nickname=nickname)
    new_relation.save()


    (con_abbr, con_title) = find_converse_relation(user1, relation)

    converse_relation = Relationship(
        user_from=user2, user_to=user1,
        relation=con_abbr
    )
    converse_relation.save()

    update_contract_list(user1, user2, relation, nickname)
    update_contract_list(user2, user1, con_title, None)


def find_converse_relation(user_from, relation):
    '''
    Based on the given user name, and its conversed relation.
    for example:
        user_from call user_to 'husband'
        so the return relation is 'wife'
    '''
    relation = RelationValue.objects.filter(title=relation)[0]
    user = User.objects.filter(phone=user_from)[0]

    abbr = None
    title = None

    if user.is_male():
        abbr = relation.cma
        title = relation.cmt
    else:
        abbr = relation.cfa
        title = relation.cft
    return (abbr, title)


def update_contract_list(user1, user2, relation, nickname):
    '''
    Updates the contract list. Make user1 and user2 to be friend.
    '''
    user = User.objects.get(phone=user1)
    friend = User.objects.get(phone=user2)
    user_id = user.id
    friend_id = friend.id
    friendship = Contract(
        user_id=user_id, friend_id=friend_id,
        friend_name=friend.nickname,
        friend_phone=user2, remark_name=relation, first_char='C',
        remark_tags=relation)

    friendship.save()


def get_contract(user_account):
    '''
    Gets one person's all contract.
    '''
    user_set = User.objects.filter(phone=user_account)
    user_id = user_set[0].id
    contracts = Contract.objects.filter(user_id=user_id)
    serializer = ContractSerilizer(contracts, many=True)
    return serializer.data
