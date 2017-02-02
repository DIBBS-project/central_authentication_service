# coding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

from rest_framework import serializers
# import django.contrib.auth

from .models import Token


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Token
        fields = ('username', 'token', 'created')
        read_only_fields = ('username', 'token', 'created')
#         extra_kwargs = {
#             'password': {'write_only': True}
#         }
