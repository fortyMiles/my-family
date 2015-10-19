from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from account import views

urlpatterns = [
    url(r'login/', views.user_login, name='login'),
    url(r'get-code/', views.get_verification_code, name='get-verification-code'),
    url(r'register/', views.register, name='register'),
    #url(r'^get-code$', views.get_verification_code, name='get-vericifation-cod,
#    url(r'^register$', views.register, name='register'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
