import base64
import json

import requests
from rest_framework import serializers
# import django.contrib.auth

from . import remote
from .models import Credential, Token, deobfuscate


class CredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credential
        fields = ('id', 'name', 'site', 'user', 'created', 'credentials')
        read_only_fields = ('id', 'user')
        extra_kwargs = {
            'credentials': {'write_only': True}
        }

    def validate_site(self, name):
        try:
            site_data = remote.site(name)
        except requests.HTTPError as e:
            raise serializers.ValidationError("Site not found")
        return name

    def validate_credentials(self, value):
        try:
            cred_data = deobfuscate(value)
        except (json.decoder.JSONDecodeError, UnicodeDecodeError):
            raise serializers.ValidationError("Invalid base64-encoded JSON")

        missing_fields = {'username', 'password', 'project_name'} - set(cred_data)
        if missing_fields:
            raise serializers.ValidationError('Missing fields: {}'.format(missing_fields))

        return value


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Token
        fields = ('username', 'token', 'created')
        read_only_fields = ('username', 'token', 'created')
#         extra_kwargs = {
#             'password': {'write_only': True}
#         }
