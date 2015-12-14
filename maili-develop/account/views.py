# -*- coding:utf-8 -*-
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account.models import User
from account.utility import send_message
from account.utility import generate_token
from .service import check_user_exist
from .service import update_user
from .service import create_new_user
from .service import get_user_info
from .service import set_user_login
from .service import save_file

# Create your views here.

POST = 'POST'
GET = 'GET'
PUT = 'PUT'


@api_view([POST])
def user_login(request):
    """
    receives post request and login user.

    [Notice], Must send password's MD5 code.

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
        phone = request.data['phone'].strip()
        password = request.data['password']

        try:
            set_user_login(account=phone, password=password)
            token = generate_token.generate_token(phone)
            return Response(
                status=status.HTTP_202_ACCEPTED,
                content={'token': token}
            )
        except NameError as e:
            print e
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print e
            return Response(status=status.HTTP_400_BAD_REQUEST)


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

    context = {"code": None}

    if success:
        resp_status = status.HTTP_200_OK
        context['code'] = code
    else:
        resp_status = status.HTTP_408_REQUEST_TIMEOUT

    return Response(context, status=resp_status)


@api_view([GET])
def test_exist(request, name):
    """
    Test a user if is register already.

    - returns:

        {'exist': Boolean}

    """
    exist = check_user_exist(name)
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
    data = get_user_info(username)

    if data:
        return Response({'data': data}, status=200)
    else:
        return Response(status=404)


class UserAccount(APIView):
    """
    Creates or updates a user.

    """

    def post(self, request):
        """
        Create a new user.

        data:

        {
        "phone":varchar(), // require: True
        "password":md5_varchar(),
        "first_name":varchar(),
        "gender":varchar(), // ('M', 'F', 'U')
        "marital_status":varchar(), // (true, false)
        "nickname": varchar()
        }

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

        - name: nickname
          description: nickname
          required: false
          type: string
          parameType: form
        """

        try:
            request.POST._mutable = True
            post_data = request.data.copy()
            create_new_user(data=post_data)
            return Response(status=202)
        except Exception as e:
            print e
            return Response(status=409)

    def put(self, request):
        """
        Update an existed user.

        data:

        {
        "phone":varchar(), // require: True
        "password":md5_varchar(),
        "first_name":varchar(),
        "gender":varchar(), // ('M', 'F', 'U')
        "marital_status":varchar(), // (true, false)
        "nickname": varchar()
        }

        ---
        parameters:
        - name: first_name
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

        - name: marital_status
          description: if married
          required: false
          type: string
          paramType: form

        - name: nickname
          description: if married
          required: false
          type: string
          paramType: form
        """
        try:
            request.POST._mutable = True
            post_data = request.data.copy()
            update_user(data=post_data)
            return Response(status=202)
        except Exception as e:
            print e
            return Response(status=407)


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
            return Response({'url': photo_url}, status=status.HTTP_200_OK)
        else:
            return Response(status=404)

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

        binary_data = request.data.get('photo', None)

        try:
            photo_url = save_file(binary_data)
            set_user_login(user_name, photo_url)
            return Response(
                {'url': photo_url},
                status=202
            )
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
