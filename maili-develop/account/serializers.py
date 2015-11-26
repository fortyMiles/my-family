from account.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100, required=False)
    first_name = serializers.CharField(max_length=20, required=False)
    gender = serializers.CharField(max_length=2, required=False)
    marital_status = serializers.BooleanField(required=False)
    nickname = serializers.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ('phone', 'password', 'first_name',
                  'gender', 'marital_status', 'nickname')


