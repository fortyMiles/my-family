# -*- coding: utf-8 -*-
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from relation.service import check_user_exist
from relation.service import check_relation_exist
from relation.service import check_relation_accept
from relation.service import create_relation
from relation.service import get_contract


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

        data:

            {
            "user1": varchar(), // user1 is 小明
            "user2": varchar(), // user2 is his mother
            "relation": varchar() // relation is 母亲
            "nickname": nickname  // required == false
            }

        return:

            - 201: relation created.
            - 406: Relation is not acceptable
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
          description: relation is 妈妈
          required: true
          type: string
          paramters: form

        - name: nickname
          description: nickname is 围裙妈妈
          required: false
          type: string
          paramters: form
        """

        user1 = request.data.get('user1', None)
        user2 = request.data.get('user2', None)
        relation = request.data.get('relation', None)
        nickname = request.data.get('nickname', None)

        user1_exist = check_user_exist(user1)
        user2_exist = check_user_exist(user2)

        if not user1_exist or not user2_exist:
            return Response({'status': status.HTTP_404_NOT_FOUND})
        elif check_relation_exist(user1, user2):
            return Response({'status': status.HTTP_409_CONFLICT})
        elif not check_relation_accept(relation):
            return Response({'status': status.HTTP_406_NOT_ACCEPTABLE})
        else:
            create_relation(user1, user2, relation, nickname)
            return Response({'status': status.HTTP_201_CREATED})


@api_view(['GET'])
def contract_list(request, name):
    """
    Gets one person's all friends in his/her contract.
    """
    try:
        data = get_contract(user_account=name)
        return Response({'status': status.HTTP_200_OK,
                         'data': data})
    except Exception as e:
        print e
        return Response({'status': status.HTTP_400_BAD_REQUEST})
