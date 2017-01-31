# coding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'tokens', views.TokenViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
