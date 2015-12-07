from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from home.service import get_home_info
from home.service import get_joined_home_info

# Create your views here.

@api_view(['GET'])
def home_info(request, home_id):
    pass


@api_view(['GET'])
def home_info_list(request, username):
    pass

