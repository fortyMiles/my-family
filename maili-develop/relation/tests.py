# -*- coding: utf-8 -*-
from django.test import TestCase
from relation.models import RelationValue
from account.models import User


class TestRelationService(TestCase):

    def setUp(self):
        minchiuan = User(
            phone='18857453090',
            password='12345678910',
            last_name='高')

        lily = User(phone='18668831228', password='12345678910', last_name='粒')
        minchiuan.save()
        lily.save()

    def test_check_user_exist(self):
        pass
