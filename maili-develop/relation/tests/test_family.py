# -*- coding: utf-8 -*-
from django.test import TestCase
from relation.models import Relationship
from account.models import User
from relation.utility import build_model

class TestFamilyBuild(TestCase):

    def setUp(self):
        build_model.build_model()
        pass

