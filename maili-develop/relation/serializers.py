from rest_framework import serializers
from .models import Contract


class ContractSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ('friend_name', 'friend_phone',
                  'remark_name', 'first_char',
                  'remark_tags', 'relation',
                  'avatar')
