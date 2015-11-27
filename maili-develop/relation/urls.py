from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from relation import views

urlpatterns = [
    url(r'create/', views.Relation.as_view()),
    url(r'contract/(?P<name>[a-z0-9]+)/', views.contract_list, name='contract'),
    url(r'home_member/(?P<name>[a-z0-9]+)/', views.home_member_list, name='home'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
