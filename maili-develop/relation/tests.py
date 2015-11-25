from django.test import TestCase

# Create your tests here.

from relation.utility import build_model


class TestDataBuild(TestCase):
    build_model.build_model()
