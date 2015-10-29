from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from account import views

urlpatterns = [
    url(r'login/', views.user_login, name='login'),
    url(r'captcha/', views.get_verification_code, name='get-verification-code'),
    url(r'register/', views.register, name='register'),
    url(r'relation/', views.update_relation_list, name='relation'),
    url(r'contract/(?P<name>[a-z0-9]+)/', views.contract, name='contract'),
    url(r'avator/', views.Avator.as_view(), name='avator'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
