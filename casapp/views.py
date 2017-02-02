# coding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

import json
import logging

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Token
from .serializers import TokenSerializer

logger = logging.getLogger(__name__)

GENERIC_FORBIDDEN = Response(
    {'error': 'invalid credentials'},
    status=status.HTTP_403_FORBIDDEN
)


class TokenView(APIView):
    def get(self, request):
        try:
            token_string = request.META['HTTP_DIBBS_AUTHORIZATION']
        except KeyError:
            return Response(
                {'error': 'no token provided'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            token = Token.objects.get(token=token_string)
        except Token.DoesNotExist:
            return GENERIC_FORBIDDEN

        return Response(
            {'username': token.user.username},
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        # serializer = TokenSerializer(request.data)
        try:
            username = request.data['username']
            password = request.data['password']
        except (TypeError, KeyError):
            return Response({'error': 'bad request'})

        user = authenticate(username=username, password=password)
        if user is None:
            return GENERIC_FORBIDDEN

        token = Token.objects.create(user=user)
        return Response({'token': token.token})
