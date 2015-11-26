# -*- coding: utf-8 -*-
from django.test import TestCase
from relation.models import Relationship
from account.models import User
from relation.service import check_user_exist
from relation.service import check_relation_accept
from relation.service import check_relation_exist
from relation.service import find_converse_relation
from relation.service import create_relation
from relation.service import update_contract_list
from relation.service import get_contrat
from relation.utility import build_model


class TestRelationService(TestCase):

    def setUp(self):
        phone1 = '18857453090'
        phone2 = '18668831228'

        minchiuan = User(phone=phone1,
                         password='12345678910',
                         gender='M',
                         last_name='高')

        lily = User(phone=phone2,
                    password='12345678910',
                    gender='F',
                    last_name='粒')

        hua = User(phone='18868103391',
                   password='12345678910',
                   gender='F',
                   last_name='粒')

        minchiuan.save()
        lily.save()
        hua.save()

        relationship = Relationship(user_from=phone1, user_to=phone2,
                                    relation=u'哥哥')
        relationship.save()

        build_model.build_model()

    def test_check_user_exist(self):
        user1 = '18857453090'
        user2 = '18857453091'

        exist = check_user_exist(user1)
        self.assertEqual(exist, True)

        exist = check_user_exist(user2)
        self.assertEqual(exist, False)

    def test_relation_exist(self):
        user1 = '18857453090'
        user2 = '18668831228'
        user3 = '18857453091'

        exist = check_relation_exist(user1, user2)
        self.assertTrue(exist)

        exist = check_relation_exist(user1, user3)
        self.assertFalse(exist)

    def test_relation_accept(self):
        relation = u'哥哥'

        accept = check_relation_accept(relation)
        self.assertEqual(accept, True)

        relation = u'大哥哥'
        accept = check_relation_accept(relation)
        self.assertEqual(accept, False)

    def test_converse_relation(self):
        user_from = '18857453090'
        (convser_abbr, convser_title) = find_converse_relation(user_from, '哥哥')
        self.assertEquals(convser_abbr, 'CA')

        user_from = '18668831228'
        (convser_abbr, convser_title) = find_converse_relation(user_from, '母亲')
        self.assertEquals(convser_abbr, 'BC')

    def test_create_relation(self):
        user_from = '18868103391'
        user_to = '18857453090'
        create_relation(user1=user_from, user2=user_to,
                        relation='爷爷', nickname='偶吧')

        relation = Relationship.objects.filter(user_from=user_from,
                                               user_to=user_to)[0]

        self.assertEqual(relation.relation, 'EA')

        converse_relation = Relationship.objects.filter(user_from=user_to,
                                                        user_to=user_from)[0]

        self.assertEqual(converse_relation.relation, 'DB')

    def test_update_contract_list(self):
        phone1 = '18857453090'
        phone2 = '18668831228'

        update_contract_list(
            user1=phone1, user2=phone2,
            relation='妹妹', nickname='蛋蛋'
        )

        data = get_contract(phone1)
        print(data)

