# coding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

from django.conf.urls import include, url
from django.contrib import admin
# from rest_framework.routers import DefaultRouter
# import rest_framework.authtoken.views
# import allauth.urls as allauth_urls

admin.autodiscover()

urlpatterns = [
    url(r'^auth/', include('casapp.urls')),
    # url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
