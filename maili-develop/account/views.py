# -*- coding:utf-8 -*-
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.contrib.auth import authenticate, login
from account.serializers import UserSerializer
from account.serializers import FriendshipSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from account.models import User
from account.models import Relationship
from account.models import Friendship
from rest_framework.renderers import JSONRenderer
import json
from account.utility import send_message
# Create your views here.

POST = 'POST'
GET = 'GET'


@api_view([POST])
def user_login(request):
    """
    receives post request and login user.

    args:

        data: user login information
        {
        "phone":varchar(),
        "password":md5_varchar()
        }

    return:

    - code: *202*
      message: information is correct, and user has login
    - code: *401*
      message: name or password error.

    ---
    parameters:
    - name: phone
      description: user's phone number
      required: true
      type: string
      paramType: form

    - name: password
      description: user's password
      required: true
      type: string
      paramType: form

    """
    # import pdb; pdb.set_trace()
    if request.method == 'POST':
        phone = request.data['phone']
        password = request.data['password']
        user_set = User.objects.filter(phone=phone).filter(password=password)
        if user_set:
        #    login(user_set[0])
            user_set[0].is_login = True
            return Response({'status': status.HTTP_202_ACCEPTED})
        else:
            return Response({'status': status.HTTP_401_UNAUTHORIZED})


@api_view([POST])
def get_verification_code(request):
    """
    get a verification code from server.

    args:

        data: phoen number of user input.
        {
            "phone":varchar()
        }

    returns:

    - staus
    - code

    ---
    parameters:
    - name: phone
      description: User's phone number
      required: true
      type: string
      paramType: form
    """

    # phone = request.query_params['phone']

    phone = (request.data['phone'])
    code = send_message.random_code(phone)
    success = send_message.send_message(phone, code)

    context = {"status": None, "code:": None}

    if success:
        context['status'] = status.HTTP_200_OK
        context['code'] = code
    else:
        context['status'] = status.HTTP_408_REQUEST_TIMEOUT

    return Response(context)


@api_view([POST])
def register(request):
    """
    registers a new user account by phone number and password

    args:

        data: user register inforamtion
        {
            "firstName":varchar(),
            "password":md5_varchar(),
            "mobilePhone":varchar(),
            "gender":varchar(),
            "maritalStatus":varchar()
        }

    - returns:

        HTTP status code: 200, login succeed

    ---
    parameters:
        - name: firstName
          description: first name
          required: true
          type: string
          paramType: form

        - name: password
          description: password
          required: true
          type: string
          paramType: form

        - name: mobilePhone
          description: phone number
          required: true
          type: string
          paramType: form

        - name: gender
          description: gender
          required: true
          type: string
          paramType: form

        - name: maritalStatus
          description: if married
          required: true
          type: string
          paramType: form

    """
    try:
        firstName = request.data.get('firstName', 'TEST')# ['firstName']
        password = request.data.get('password', 'password')
        mobilePhone = request.data.get('mobilePhone', '12345678910')
        gender = request.data.get('gender', 'F')
        maritalStatus = request.data.get('maritalStatus', 'false')
        user = User(phone=mobilePhone, password=password, first_name=firstName, gender=gender, marital_status=maritalStatus)
        user.save()

        return Response({'status': status.HTTP_201_CREATED})
    except Exception as e:
        print e
        return Response({'status': status.HTTP_409_CONFLICT})


@api_view([POST])
def update_relation_list(request):
    '''
    Updates relationship list.


    args:

        data: relationship. Refine what's relation of user1 and user2.
        for example, user1 is user2's mother, the realtion will be mother,
        so the data will be {'user1':'someone', 'user2':'someone2', 'relation':'mother'},
        if we exchange the user1's and user2's name, which to be {'user1':'someone2','user2':'someone', 'relation':'son'}

        {
        "user1":varchar(),
        "user2":varchar(),
        "relation":varchar()
        }

    return:

    - *http 201*
      message is corrent and user's relation has been created.

    - *http 401*
      some information is error. Relation has not been created.


    ---
    parameters:
    - name: user1
      descritpion: first user's account
      required: true
      type: string
      parameType: form

    - name: user2
      descritpion: second user's account
      required: true
      type: string
      parameType: form

    - name: relation
      descritpion: what's the relation from user1 to user2.
      required: true
      type: string
      parameType: form
    '''
    try:
        user1 = request.data.get('user1', 'TEST')
        user2 = request.data.get('user2', 'TEST')
        relation = request.data.get('relation', 'TEST')

        from_user = User.objects.filter(phone=user1)
        to_user = User.objects.filter(phone=user1)
        if from_user and to_user:
            from_user_id = from_user[0].id
            to_user_id = to_user[0].id
            relationship = Relationship(from_user_id=from_user_id, to_user_id=to_user_id, relation=relation)
            relationship.save()

            update_contract_list(user1, user2, relation)
            update_contract_list(user2, user1, relation)

            return Response({'status': status.HTTP_201_CREATED})
    except Exception as e:
        print e
        return Response({'status': status.HTTP_400_BAD_REQUEST})



def update_contract_list(username, to_user, relation):
    user = User.objects.filter(phone=username)[0]
    friend = User.objects.filter(phone=to_user)[0]

    user_id = user.id
    friend_id = friend.id

    friend_name = friend.first_name
    if friend.full_name:
        friend_name = friend.full_name
    if friend.nickname:
        friend_name = friend.nickname

    remark_name = friend_name
    first_char = 'T'
    remark_tags = '亲属'
    friend = Friendship(
        user_id=user_id, friend_id=friend_id,
        friend_phone=to_user, friend_name=friend_name,
        remark_name=remark_name, first_char=first_char,
        remark_tags=remark_tags)
    friend.save()


@api_view([GET])
def contract(request, name):
    """
    Gets one person's all friends in his/her contract.
    """
    if request.method == GET:
        try:
            user = User.objects.filter(phone=name)
            user_id = user[0].id
            friends = Friendship.objects.filter(user_id=user_id)
            serializer = FriendshipSerializer(friends, many=True)
            return Response({'status': status.HTTP_200_OK, 'data': serializer.data})
        except Exception as e:
            print e
            return Response({'status': status.HTTP_400_BAD_REQUEST})


class Avator(APIView):
    """
    saves avator and gets person's avator.
    """
    def get(self, request, user_name):
        '''
        gets one's avator url.

        returns:

            {'status': HTTP sattus, 'url': avator's url}
        '''
        user_set = User.objects.filter(phone=user_name)
        photo_url = None
        if user_set:
            user = user_set[0]
            photo_url = user.avator
            return Response({'status': status.HTTP_200_OK, 'url': photo_url})
        else:
            return Response({'status': status.HTTP_404_NOT_FOUND})

    def post(self, requestm, user_name):
        """
        updates one person's avator.

        datas:

            {'photo':binary_data}

        returns:

            https status

        ---
        parameters:
        - name: photo
        descritpion: phote's binary data
        required: true
        type: binary
        parameType: form
        """
        pass
