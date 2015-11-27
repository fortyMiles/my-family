# -*- coding: utf-8 -*-
from django.test import TestCase
from scope.service import update_user_scope
from scope.service import update_scope_group
from scope.service import get_home_member
from scope.models import ScopeGroup
from scope.models import Scope
from account.tests import import_users
from relation.utility import build_model
from relation.service import get_friend_information
from relation.service import create_relation

# Create your tests here.

class TestScopeService(TestCase):
    def setUp(self):
        import_users.read_user_infor_from_file(self.client)
        build_model.build_model()

    def test_update_scope_group(self):
        user1 = '18868103391'
        user2 = '17862710056'
        tag = 'home'

        update_scope_group(user1, user2, tag)

        scope_group = ScopeGroup.objects.filter(member=user2)
        self.assertEqual(len(scope_group), 1)

    def test_update_user_scope(self):
        user1 = '18868103391'
        user2 = '17862710056'
        scope = 'H'
        relation = '姐姐'

        update_user_scope(user1, user2, scope, relation)

        # test user2 in user1's home.
        scope_name = Scope.objects.filter(owner=user1).filter(tag='home')[0].scope
        scope_group = ScopeGroup.objects.filter(member=user2)[0].scope
        self.assertEquals(scope_name, scope_group)

        # test user1 in user2's home
        scope_name = Scope.objects.filter(owner=user2).filter(tag='home')[0].scope
        scope_group = ScopeGroup.objects.filter(member=user1)[0].scope
        self.assertEquals(scope_name, scope_group)

        ##############################################################
        user1 = '18868103391'
        user2 = '13375746248'
        scope = 'H'
        relation = '姐姐'

        update_user_scope(user1, user2, scope, relation)

        # test user2 in user1's home.
        scope_name = Scope.objects.filter(owner=user1).filter(tag='home')[0].scope
        scope_group = ScopeGroup.objects.filter(member=user2)[0].scope
        self.assertEquals(scope_name, scope_group)

        # test user1 not in user2's home, but in user2's relation
        scope_name = Scope.objects.filter(owner=user2).filter(tag='relation')[0].scope
        scope_group = ScopeGroup.objects.filter(member=user1)[1].scope
        self.assertEquals(scope_name, scope_group)

        ################################################################
        user1 = '18215198020'
        user2 = '18616220518'
        scope = 'R'
        relation = '表姐'

        update_user_scope(user1, user2, scope, relation)

        # test user2 in user1's relation
        scope_name = Scope.objects.filter(owner=user1).filter(tag='relation')[0].scope
        scope_group = ScopeGroup.objects.filter(member=user2).filter(tag='relation')[0].scope
        self.assertEquals(scope_name, scope_group)

        # test user1 not in user2's home, but in user2's relation
        scope_name = Scope.objects.filter(owner=user2).filter(tag='relation')[0].scope
        scope_group = ScopeGroup.objects.filter(member=user1).filter(tag='relation')[0].scope
        self.assertEquals(scope_name, scope_group)

        ################################################################
        user1 = '15700078959'
        user2 = '18616782457'
        scope = 'F'
        relation = '表姐'

        update_user_scope(user1, user2, scope, relation)

        # test user2 in user1's friend
        scope_name = Scope.objects.filter(owner=user1).filter(tag='friend')[0].scope
        scope_group = ScopeGroup.objects.filter(member=user2).filter(tag='friend')[0].scope
        self.assertEquals(scope_name, scope_group)

        # test user1 not in user2's home, but in user2's friend
        scope_name = Scope.objects.filter(owner=user2).filter(tag='friend')[0].scope
        scope_group = ScopeGroup.objects.filter(member=user1).filter(tag='friend')[0].scope
        self.assertEquals(scope_name, scope_group)

    def test_get_home_member(self):
        user1 = '18868103391'
        user2 = '17862710056'
        scope = 'H'
        relation = '姐姐'

        create_relation(user1, user2, relation, 'test')

        update_user_scope(user1, user2, scope, relation)

        user1 = '18868103391'
        user2 = '13375746248'
        scope = 'H'
        relation = '姐姐'

        create_relation(user1, user2, relation, 'test')

        update_user_scope(user1, user2, scope, relation)

        data = get_home_member(user1)
        self.assertIsNotNone(data)

        friends_information = get_friend_information(data)
        import pdb; pdb.set_trace()
        print friends_information
        self.assertIsNotNone(friends_information)
