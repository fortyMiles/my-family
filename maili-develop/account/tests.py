# -*- coding: utf-8 -*-
from django.test import TestCase
from .service import create_new_user
from .service import update_user
from .models import User
from feed.models import FeedGroup

# Create your tests here.


class AccountServiceFunctionTest(TestCase):

    def setUp(self):
        self.name = '18868103391'
        self.password = 'miffy31415926'
        self.first_name = u'高'
        self.gender = 'M'
        self.marital_status = False

        self.new_data = {
            'phone': self.name,
            'password': self.password,
            'first_name': self.first_name,
            'gender': self.gender,
            'marital_status': self.marital_status
        }

        self.update_data = {
            'phone': self.name,
            'marital_status': True
        }

    def test_create_user(self):
        create_new_user(self.new_data)

        user = User.objects.get(phone=self.name)
        group_set = FeedGroup.objects.filter(creator=self.name)
        self.assertEqual(len(group_set), 3)
        for g in group_set:
            print g.group_id
            print g.tag

        self.assertIsNotNone(user)


class AccountViewTest(TestCase):
    '''
    Test cases of account.view
    '''

    def setUp(self):
        self.name = '18868103391'
        self.password = 'miffy31415926'
        self.first_name = u'高'
        self.gender = 'M'
        self.marital_status = False

        self.new_data = {
            'phone': self.name,
            'password': self.password,
            'first_name': self.first_name,
            'gender': self.gender,
            'marital_status': self.marital_status
        }

        self.update_data = {
            'phone': self.name,
            'marital_status': True
        }

    def test_get_verification (self):
        post = {
            'phone': 18857453090
        }

        url = '/account/captcha/'
        resp = self.client.post(url, self.new_data)
        print resp

    def test_register(self):
        user = User.objects.filter(phone=self.name)
        self.assertEqual(len(user), 0)

        url = '/account/user/'
        resp = self.client.post(url, self.new_data)
        data = resp.data
        self.assertEqual(data['status'], '202')
        user = User.objects.filter(phone=self.name)
        self.assertEqual(len(user), 1)


