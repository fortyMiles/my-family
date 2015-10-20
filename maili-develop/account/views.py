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
# Create your views here.

POST = 'POST'
GET = 'GET'


@api_view([POST])
def user_login(request):
    """
    receives post request and login user.
    ---
    parameters:
    - name: phone
      description: user's name, send from request POST method.
      required: true
      type: string
      paramType: form

    - name: password
      description: user's password, send from request POST method.
      required: true
      type: string
      paramType: form

    responseMessage:
    - code: 202
      message: information is correct, and user has login
    - code: 401
      message: name or password error.
    """
    # import pdb; pdb.set_trace()
    if request.method == 'POST':
        phone = request.data['phone']
        password = request.data['password']
        user_set = User.objects.filter(phone=phone).filter(password=password)
        if user_set:
        #    login(user_set[0])
            user_set[0].is_login = True
            return Response({status.HTTP_202_ACCEPTED: 'logined'})
        else:
            return Response({status.HTTP_401_UNAUTHORIZED: 'failded'})


@api_view([POST])
def get_verification_code(request):
    """
    get a verification code from server.
    ---
    parameters:
    - name: phone
      description: User's phone number
      required: true
      type: string
      paramType: form
    """

    # phone = request.query_params['phone']

    phone = request.data['phone']
    code = phone[-6:]
    context = {"code": code}
    return Response(context)


@api_view([POST])
def register(request):
    """
    registers a new user account by phone number and password
    ---
    parameters:
        - name: phone
          descirption: user phone number
          required: true
          type: string
          paramType: form
        - name: password
          descirption: user's password
          required: true
          type: string
          paramType: form
    """
    phone = request.data['phone']
    password = request.data['password']
    try:
        user = User(phone=phone, password=password)
        user.save()
        return Response({status.HTTP_200_OK: 'okay'})
    except Exception as e:
        print e
        return Response({status.HTTP_409_CONFLICT: 'confilct'})



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
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register(request):
    try:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print e
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
'''
