# -*- coding:utf-8 -*-
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account.models import User
from account.models import Relationship
from account.models import Friendship
from account.utility import send_message
from account.utility import send_binary
from account.serializers import FriendshipSerializer
from .service import user_exist
from .service import update_user
from .service import create_new_user
from .service import get_user_info

# Create your views here.

POST = 'POST'
GET = 'GET'
PUT = 'PUT'


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

    context = {"status": None, "code": None}

    if success:
        context['status'] = status.HTTP_200_OK
        context['code'] = code
    else:
        context['status'] = status.HTTP_408_REQUEST_TIMEOUT

    return Response(context)


@api_view([GET])
def test_exist(request, name):
    """
    Test a user if is register already.

    - returns:

        {'exist': Boolean}

    """
    exist = user_exist(name)
    if exist:
        return Response({'exist': True})
    else:
        return Response({'exist': False})


@api_view([GET])
def get_user(request, username):
    """
    Gets a user's information.
    return:

        {
            status: HTTP status,
            name: string,
            gender: string,
            marital_status: string,
            first_name: string
        }
    """
    import pdb; pdb.set_trace()
    return Response(get_user_info(username))


class UserAccount(APIView):
    """
    Creates or updates a user.

    data:

        {
        "phone":varchar(), // require: True
        "password":md5_varchar(),
        "first_name":varchar(),
        "gender":varchar(),
        "marital_status":varchar()
        }

    """

    def post(self, request):
        """
        Create a new user.

        ---
        parameters:
        - name: first_name
          description: first name
          required: false
          type: string
          paramType: form

        - name: password
          description: password
          required: true
          type: string
          paramType: form

        - name: phone
          description: phone number
          required: true
          type: string
          paramType: form

        - name: gender
          description: gender
          required: false
          type: string
          paramType: form

        - name: marital_status
          description: if married
          required: false
          type: string
          paramType: form
        """

        try:
            create_new_user(data=request.data)
            return Response({'status': '202'})
        except Exception as e:
            print e
            return Response({'status': '407'})

    def put(self, request):
        """
        Update an existed user.
        ---
        parameters:
        - name: firstName
          description: first name
          required: false
          type: string
          paramType: form

        - name: password
          description: password
          required: false
          type: string
          paramType: form

        - name: phone
          description: phone number
          required: true
          type: string
          paramType: form

        - name: gender
          description: gender
          required: false
          type: string
          paramType: form

        - name: maritalStatus
          description: if married
          required: false
          type: string
          paramType: form
        """
        try:
            update_user(data=request.data)
            return Response({'status': '202'})
        except Exception as e:
            print e
            return Response({'status': '407'})


@api_view([POST])
def update_relation_list(request):
    '''
    Updates relationship list.


    args:

        data: relationship. Redefine what's relation of user1 and user2.
        for example, user1 is user2's mother, the realtion will be mother,
        so the data will be {'user1':'someone', 'user2':'someone2',
        'relation':'mother'},
        if we exchange the user1's and user2's name, which to be
        {'user1':'someone2','user2':'someone', 'relation':'son'}

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

    - name: nickname
      descritpion: what nickname user1 called user2
      type: string
      parameType: form

    '''
    # import pdb; pdb.set_trace()

    try:
        user1 = request.data.get('user1', 'TEST')
        user2 = request.data.get('user2', 'TEST')
        relation = request.data.get('relation', 'TEST')
        nickname = request.data.get('nickname', 'TEST')

        from_user = User.objects.filter(phone=user1)
        to_user = User.objects.filter(phone=user1)
        if from_user and to_user:
            from_user_id = from_user[0].id
            to_user_id = to_user[0].id
            relationship = Relationship(
                from_user_id=from_user_id,
                to_user_id=to_user_id,
                relation=relation)
            relationship.save()

            update_contract_list(user1, user2, relation, nickname)
            update_contract_list(user2, user1, relation,
                                 from_user[0].first_name)

            return Response({'status': status.HTTP_201_CREATED})
    except Exception as e:
        print e
        return Response({'status': status.HTTP_400_BAD_REQUEST})


def update_contract_list(username, to_user, relation, remark_name):
    user = User.objects.filter(phone=username)[0]
    friend = User.objects.filter(phone=to_user)[0]

    user_id = user.id
    friend_id = friend.id

    friend_name = friend.first_name
    if friend.full_name:
        friend_name = friend.full_name
        if friend.nickname:
            friend_name = friend.nickname

    first_char = 'T'
    remark_tags = relation
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
            return Response({'status': status.HTTP_200_OK,
                             'data': serializer.data})
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

    def post(self, request, user_name):
        """
        updates one person's avator.

        datas:

            {'photo':binary_data}

        returns:

            {
            'status':https status,
            'url': phote_url
            }


        ---
        parameters:
            - name: photo
            descritpion: phote's binary data
            required: true
            type: binary
            parameType: form
            """

        user_set = User.object.filter(phone=user_name)
        binary_data = request.data.get('photo', None)

        if user_set and binary_data:
            photo_url = send_binary.FileSender.send_file(binary_data)
            user = user_set[0]
            user.avator = photo_url
            user.save()
            return Response(
                {'status': status.HTTP_202_ACCEPTED, 'url': photo_url}
            )
        elif not user_set:
            return Response({'status': status.HTTP_404_NOT_FOUND})
        else:
            return Response({'status': status.HTTP_400_BAD_REQUEST})
