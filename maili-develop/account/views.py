from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.contrib.auth import authenticate, login
from account.serializers import UserSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from account.models import User
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



class UserViewSet(viewsets.ModelViewSet):
    """
    Get method, to get a user information;
    POST method, to create a user, which means, created a new user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

'''
@api_view(['POST'])
def get_verification_code(request):
    """
    get a verifcation code from server.
    """
    import pdb; pdb.set_trace()  # XXX BREAKPOINT
    try:
        phone = request.data["phone"]
        code = phone[-6:]
        response = {"code": code}
        return Response(response)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST})


@api_view(['POST'])
def register(request):
    try:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED})
        else:
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST})
    except Exception as e:
        print e
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST})
'''
