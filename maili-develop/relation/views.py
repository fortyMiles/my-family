# -*- coding: utf-8 -*-
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account.service import check_user_exist
from relation.service import check_relation_exist
from relation.service import check_relation_accept
from relation.service import create_relation
from relation.service import get_contract
from relation.service import get_friend_information
from scope.service import update_user_scope
from scope.service import get_home_member
from scope.service import get_home_id
from scope.service import get_relation_id
from scope.service import get_global_id
from scope.service import get_all_join_scope
from scope.service import get_home_creator
from relation.service import get_chinese_relation


class Relation(APIView):
    """
    Creates or Updates a relation.

    """

    def post(self, request):
        """
        Create a relation between two person.

        Support Type List:
            (
            妻子 丈夫 儿子 女儿 弟弟 哥哥 妹妹 姐姐 父亲 母亲
            孙子 孙女 女婿 媳妇 爷爷 奶奶 岳父 岳母 公公 婆婆
            朋友
            )

        ata:

            {
            "user1": varchar(), // user1 is 小明
            "user2": varchar(), // user2 is his mother
            "relation": varchar() // relation is 母亲
            "scope": <F, H, R>
            // if this person is your family, send H, means Home
            // if is other relations, send R, means Relation.
            //If this person is your friend, not
            // your any relation but is your friend. send F, means Friend
            "nickname": nickname  // required == false
            }

        return:

            - 201: relation created.
            - 406: Relation or Scope is not acceptable
            - 409: the relation is already existd.
            - 404: the user is not found.

        ---
        parameters:
        - name: user1
          description: user1 is 小明
          required: true
          type: string
          paramters: form

        - name: user2
          description: user1 is 妈妈
          required: true
          type: string
          paramters: form

        - name: relation
          description: relation is 母亲
          required: true
          type: string
          paramters: form

        - name: nickname
          description: nickname is 围裙妈妈
          required: false
          type: string
          paramters: form

        - name: scope
          description: scope is H
          required: true
          type: string
          parameters: form
        """

        user1 = request.data.get('user1', None)
        user2 = request.data.get('user2', None)
        relation = request.data.get('relation', None)
        nickname = request.data.get('nickname', 'Nickname')
        scope = request.data.get('scope', None)

        user1_exist = check_user_exist(user1)
        user2_exist = check_user_exist(user2)

        if not user1_exist or not user2_exist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        elif check_relation_exist(user1, user2):
            return Response(status=status.HTTP_409_CONFLICT)
        elif not check_relation_accept(relation):
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            create_relation(user1, user2, relation, nickname)
            update_user_scope(user1, user2, scope, relation)
            return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
def contract_list(request, name):
    """
    Gets one person's all friends in his/her contract.
    """

    try:
        data = get_contract(user_account=name)
        return Response({'data': data})
    except Exception as e:
        print e
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def home_member_list(request, name):
    """
    Gets one person's home member list.

    data:

        {'home_id': string;
        'data': json
        'status': http status
        }

    """

    try:
        home_member = get_home_member(name)
        data = get_friend_information(home_member)
        home_id = get_home_id(name)
        return Response({
            'data': data,
            'home_id': home_id})
    except Exception as e:
        print e
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def catch_home_id(request, name):
    """
    When send feed to 'home only.' you need to get this scope id.

    Response:

        {
        status: String,
        id: String
        }
        """

    try:
        home_id = get_home_id(name)
        return Response({
            'id': home_id
        })
    except Exception as e:
        print e
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def catch_relation_id(request, name):
    """
    When send feed to 'all relation.' you need to get this scope id.

    Response:

        {
        status: String,
        id: String
        }
        """

    try:
        _id = get_relation_id(name)
        return Response({
            'id': _id})
    except Exception as e:
        print e
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def catch_global_id(request, name):
    """
    When send feed to 'all friend.' you need to get this scope id.

    Response:

        {
        status: String,
        id: String
        }
        """

    try:
        _id = get_global_id(name)
        return Response({
            'id': _id})
    except Exception as e:
        print e
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_all_invole_scope(request, name):
    """
    Gets all involved scopes. Including the initial three scopes and
    other involved groups.
    """
    try:
        _id_list = get_all_join_scope(name)
        return Response({
            'id': _id_list
        })
    except Exception as e:
        print e
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def home_creator(request, home_id):
    """
    Get home's creator based on home_id.
    If no this home, return None
    """

    try:
        creator = get_home_creator(home_id)
        return Response({
            'creator': creator
        })
    except Exception as e:
        print e
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_chinese_relation_name(request, user1, user2):
    """
    Gets what user1 called user2 in Chinese

    Response:

        {'status': Http status,
        'title': string
        }
    """
    try:
        title = get_chinese_relation(user1, user2)
        return Response({
            'title': title
        })
    except Exception as e:
        print e
        return Response(status=status.HTTP_404_NOT_FOUND)
