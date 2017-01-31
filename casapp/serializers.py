# coding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

from rest_framework import serializers
# import django.contrib.auth

from .models import Token


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('user', 'payload', 'created')
        read_only_fields = ('payload', 'created')
#         extra_kwargs = {
#             'password': {'write_only': True}
#         }
