from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from relation import views

urlpatterns = [
    url(r'create/', views.Relation.as_view()),
    url(r'contract/(?P<name>[a-z0-9]+)/', views.contract_list, name='contract'),
    url(r'home_member/(?P<name>[a-z0-9]+)/', views.home_member_list, name='home'),
    url(r'home_id/(?P<name>[a-z0-9]+)/', views.catch_home_id, name='home'),
    url(r'relation_id/(?P<name>[a-z0-9]+)/', views.catch_relation_id, name='home'),
    url(r'friend_id/(?P<name>[a-z0-9]+)/', views.catch_global_id, name='home'),
    url(r'invole/(?P<name>[a-z0-9]+)/', views.get_all_invole_scope, name='home'),
    url(r'home_creator/(?P<home_id>[a-z0-9]+)/', views.home_creator, name='home'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
