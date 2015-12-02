# -*- coding: utf-8 -*
from django.test import TestCase
from account.service import create_new_user
from account.service import update_user
from account.service import get_user
from account.service import user_has_married
from account.service import create_avatar
from account.service import get_avatar
from account.models import User
from account.tests import import_users
from feed.models import FeedGroup
from scope.models import Scope

# Create your tests here.


class AccountServiceFunctionTest(TestCase):

    def setUp(self):
        self.name = '18857453090'
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

    def test_update_user(self):
        create_new_user(self.new_data)
        update_user(self.update_data)
        user_set = User.objects.filter(phone=self.name)
        self.assertEqual(len(user_set), 1)
        self.assertEqual(user_set[0].marital_status, True)
        self.assertIsNotNone(user_set[0].avatar)

    def test_get_user(self):
        user_phone = '18857453090'
        create_new_user(self.new_data)
        user = get_user(user_phone)

        user_phone = '18857453099'
        user = get_user(user_phone)
        self.assertEqual(user, None)

    def test_is_married(self):
        self.new_data['marital_status'] = True
        create_new_user(self.new_data)
        married = user_has_married('18857453090')
        self.assertEqual(married, True)

    def test_get_avatar(self):
        pic = get_avatar('F', False)
        self.assertIsNotNone(pic)
        self.assertEqual(pic, "4ce4a9bd31646c9d05c0226c2df0d2a3.png")

    def test_create_avator(self):
        data = create_avatar(self.new_data)
        self.assertIsNotNone(data['avatar'])
        print(data['avatar'])


class AccountViewTest(TestCase):
    '''
    Test cases of account.view
    '''

    def setUp(self):
        self.name = '15557453391'
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

    '''
    def test_get_verification (self):
        post = {
            'phone': 18857453090
        }

        url = '/account/captcha/'
        resp = self.client.post(url, self.new_data)
        print resp
    '''

    def test_register(self):

        import_users.read_user_infor_from_file(self.client)
        user = User.objects.filter(phone=self.name)
        self.assertEqual(len(user), 0)

        url = '/account/user/'
        resp = self.client.post(url, self.new_data)
        data = resp.data
        self.assertEqual(data['status'], '202')
        user = User.objects.filter(phone=self.name)
        self.assertEqual(len(user), 1)
        scope_set = Scope.objects.filter(owner='18868103391')
        for s in scope_set:
            print s.scope

        self.assertEqual(len(scope_set), 3)
        self.assertNotEquals(scope_set[0].scope, scope_set[1].scope)
        self.assertNotEquals(scope_set[1].scope, scope_set[2].scope)
