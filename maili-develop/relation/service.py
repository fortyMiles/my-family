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
    check_relation_exist(user1, user2)
    check_relation_accept(relation)


def create_relation(user1, user2, relation, nickname):
    """
    Based on user1 and user2's name and relation of them, create a relation.
    This is for RELTATION, it means, if A and B is sister. They could be in a
    home and maybe in another home. But SISTER relation will be built first.
    """

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
        remark_tags=relation, relation=relation, avatar=friend.avatar)

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


def user_has_married(phone_number):
    user = User.objects.filter(phone=phone_number)[0]
    return user.marital_status


def is_close_family_member(user1, user2, relation):
    close = False
    if relation_distance(relation) <= 1:
        if not is_sibling(relation):
            close = True
        elif user_has_married(user1) or user_has_married(user2):
            close = False
        else:
            close = True
    return close


def is_sibling(relation):
    relation_abbr = RelationValue.objects.get(title=relation).abbr
    SIBLING = ['CA', 'CB', 'CC', 'CD']
    return relation_abbr in SIBLING


def relation_distance(relation):
    '''
    Gets the relation distance of this relation.
    e.g: father: 1, son:1, wife:1, grandfather: 2
    '''
    level = RelationValue.objects.get(title=relation).level
    return level


def get_friend_information(phone_number_list):
    contract_set = Contract.objects.filter(friend_phone__in=phone_number_list)
    serializer = ContractSerilizer(contract_set, many=True)
    return serializer.data
