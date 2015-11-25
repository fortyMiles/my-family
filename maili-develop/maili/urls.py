"""maili URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

# Routers provide an easy way of automatically determining the URL conf.

'''
Because we're using viewsets instead of views,
we can automatically generate the URL conf for our API,
by simply registering the viewsets with a router class.
'''

urlpatterns = [
    url(r'^account/', include('account.urls', namespace='account')),
    url(r'^relation/', include('relation.urls', namespace='account')),
    url(r'^group/', include('group.urls', namespace='group')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    # add REST framework access control.
    url(r'^docs/', include('rest_framework_swagger.urls')),
]
