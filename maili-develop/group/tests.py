from django.test import TestCase
from group.group_service import get_home_info
from account.tests import import_users
from scope.service import get_home_id
# Create your tests here.
from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from group import views

urlpatterns = patterns(
    url(r'^test/(?P<name>[0-9]+)/$', views.GroupAPI.as_view()),
    url(r'^/(?P<name>[0-9]+)/$', views.GroupAPI.as_view()),
    url(r'^member/$', views.Join.as_view()),
    url(r'^join/(?P<name>[0-9]*)/$', views.Member.as_view()),
    url(r'^home_info/(?P<name>[0-9]*)/$', views.join_home_info),
)

urlpatterns = format_suffix_patterns(urlpatterns)


class HomeInfoTest(TestCase):
    def setUp(self):
        import_users.read_user_infor_from_file(self.client)

    def test_get_home_info(self):
        username = '18868103391'
        groups_list = get_home_id(username)
        print groups_list
        self.assertIsNotNone(groups_list)

        group = groups_list[0]

        data = get_home_info(group)
        print data
        self.assertIsNotNone(data)
        print data['creator']
