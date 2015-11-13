from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from group import views

urlpatterns = patterns(
    url(r'^test/(?P<name>[0-9]+)/$', views.GroupAPI.as_view()),
    url(r'^/(?P<name>[0-9]+)/$', views.GroupAPI.as_view()),
    url(r'^member/$', views.Join.as_view()),
    url(r'^member/(?P<name>[0-9]*)/$', views.Member.as_view()),
)

urlpatterns = format_suffix_patterns(urlpatterns)
