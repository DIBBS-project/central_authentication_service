# coding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'credentials', views.CredentialViewSet)

urlpatterns = [
    url(r'^auth/tokens', views.TokenView.as_view()),
    url(r'^', include(router.urls)),
]
