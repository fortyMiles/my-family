from django.test import TestCase
from .service import get_feed_group_name
from .service import create_feed_group
from .service import create_default_feed_group
from .models import FeedGroup

# Create your tests here.


class FeedServiceMethodTest(TestCase):

    def setUp(self):
        self.name = '18857453090'
        self.tag1 = 'G'
        self.tag2 = 'H'

    def test_given_feed_group_name(self):
        '''
        Test give feed group name.
        '''
        group1 = get_feed_group_name(self.name, self.tag1)
        group2 = get_feed_group_name(self.name, self.tag2)

        self.assertIsNotNone(group1)
        self.assertNotEqual(group1, group2)

    def test_create_feed_group(self):
        '''
        Tests create feed group
        '''
        tags = ['G', 'H', 'F']

        for t in tags:
            create_feed_group(self.name, t)
            group = FeedGroup.objects.filter(creator=self.name, tag=t)
            self.assertIsNotNone(group)

    def test_create_defalut_feed_group(self):

        create_default_feed_group(self.name)


