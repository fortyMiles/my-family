from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from account import views

urlpatterns = [
     url(r'user/', views.UserAccount.as_view()),
     url(r'info/(?P<username>[a-z0-9]+)/', views.get_user),
     url(r'login/', views.user_login, name='login'),
     url(r'captcha/', views.get_verification_code,
         name='get-verification-code'),
     url(r'exist/(?P<name>[a-z0-9]+)/', views.test_exist, name='exist'),
     url(r'relation/', views.update_relation_list, name='relation'),
     url(r'contract/(?P<name>[a-z0-9]+)/', views.contract, name='contract'),
     url(r'avatar/(?P<user_name>[a-z0-9]+)',
         views.Avator.as_view(), name='avatar'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
