from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


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
        """

        user1 = request.data.get('user1', None)
        user1 = request.data.get('user1', None)
        user1 = request.data.get('user1', None)
        user1 = request.data.get('user1', None)
